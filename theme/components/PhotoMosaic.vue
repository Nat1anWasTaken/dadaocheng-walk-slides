<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import type { MosaicPhoto } from '../layoutHelper'
import { resolveAssetUrl } from '../layoutHelper'
import PhotoChip from './PhotoChip.vue'

const props = withDefaults(defineProps<{
  photos: (MosaicPhoto | string)[]
  /** Gap between photos in px */
  gap?: number
  /** Rounded corners (px) on each photo */
  radius?: number
  /** Force an arrangement, e.g. [1, 2] = first photo alone, then two. */
  split?: number[]
  /** Direction for `split`: 'rows' stacks groups vertically, 'cols' side by side. */
  direction?: 'rows' | 'cols'
}>(), {
  gap: 6,
  radius: 0,
})

const items = computed<MosaicPhoto[]>(() =>
  (props.photos ?? []).map(p => (typeof p === 'string' ? { src: p } : p)),
)

const natural = reactive<Record<number, number>>({})

function parseRatio(r: MosaicPhoto['ratio']): number | undefined {
  if (r == null || r === '')
    return undefined
  if (typeof r === 'number')
    return r
  if (r === 'portrait')
    return 3 / 4
  if (r === 'landscape')
    return 4 / 3
  if (r === 'square')
    return 1
  const m = String(r).match(/^\s*([\d.]+)\s*[/:x]\s*([\d.]+)\s*$/)
  if (m)
    return Number(m[1]) / Number(m[2])
  const n = Number(r)
  return Number.isFinite(n) && n > 0 ? n : undefined
}

const ratios = computed(() => items.value.map((p, i) => parseRatio(p.ratio) ?? natural[i] ?? 4 / 3))

function onLoad(i: number, e: Event) {
  const img = e.target as HTMLImageElement
  if (img.naturalWidth && img.naturalHeight)
    natural[i] = img.naturalWidth / img.naturalHeight
}

// Container size (unscaled CSS px of the slide canvas)
const root = ref<HTMLElement>()
const size = reactive({ w: 900, h: 480 })
let ro: ResizeObserver | undefined
onMounted(() => {
  if (!root.value)
    return
  const measure = () => {
    if (root.value && root.value.clientWidth > 0 && root.value.clientHeight > 0) {
      size.w = root.value.clientWidth
      size.h = root.value.clientHeight
    }
  }
  measure()
  ro = new ResizeObserver(measure)
  ro.observe(root.value)
})
onBeforeUnmount(() => ro?.disconnect())

function compositions(n: number): number[][] {
  if (n <= 0)
    return [[]]
  const out: number[][] = []
  for (let first = 1; first <= n; first++) {
    for (const rest of compositions(n - first))
      out.push([first, ...rest])
  }
  return out
}

interface Plan { dir: 'rows' | 'cols', groups: number[][] }

function groupsOf(split: number[]): number[][] {
  const groups: number[][] = []
  let i = 0
  for (const k of split) {
    groups.push(Array.from({ length: k }, (_, j) => i + j))
    i += k
  }
  return groups
}

// Pick the arrangement whose natural (uncropped) size best matches the box,
// trying every ordered split into rows and into columns.
const plan = computed<Plan>(() => {
  const n = items.value.length
  const a = ratios.value
  const g = props.gap
  if (props.split?.length)
    return { dir: props.direction ?? 'rows', groups: groupsOf(props.split) }
  let best: Plan & { cost: number } = { dir: 'rows', groups: groupsOf([n]), cost: Infinity }
  for (const split of compositions(n)) {
    const groups = groupsOf(split)
    // rows: every row spans the full width
    const hNat = groups.reduce((s, row) => s + (size.w - g * (row.length - 1)) / row.reduce((t, i) => t + a[i], 0), 0) + g * (groups.length - 1)
    const rowCost = Math.abs(Math.log(hNat / size.h)) + 0.04 * groups.length
    if (rowCost < best.cost)
      best = { dir: 'rows', groups, cost: rowCost }
    // cols: every column spans the full height
    const wNat = groups.reduce((s, col) => s + (size.h - g * (col.length - 1)) / col.reduce((t, i) => t + 1 / a[i], 0), 0) + g * (groups.length - 1)
    const colCost = Math.abs(Math.log(wNat / size.w)) + 0.04 * groups.length
    if (colCost < best.cost)
      best = { dir: 'cols', groups, cost: colCost }
  }
  return { dir: best.dir, groups: best.groups }
})

// flex-grow weights (scaled so they never sum below 1, which would leave gaps)
function rawGroupWeight(group: number[]) {
  const a = ratios.value
  return plan.value.dir === 'rows'
    ? 1 / group.reduce((t, i) => t + a[i], 0)
    : 1 / group.reduce((t, i) => t + 1 / a[i], 0)
}

function rawItemWeight(i: number) {
  const a = ratios.value[i]
  return plan.value.dir === 'rows' ? a : 1 / a
}

function groupWeight(group: number[]) {
  const total = plan.value.groups.reduce((t, g) => t + rawGroupWeight(g), 0)
  return (100 * rawGroupWeight(group) / total).toFixed(3)
}

function itemWeight(group: number[], i: number) {
  const total = group.reduce((t, j) => t + rawItemWeight(j), 0)
  return (100 * rawItemWeight(i) / total).toFixed(3)
}
</script>

<template>
  <div
    ref="root"
    class="deck-mosaic"
    :class="`deck-mosaic-${plan.dir}`"
    :style="{ gap: `${props.gap}px`, '--deck-mosaic-radius': `${props.radius}px` }"
  >
    <div
      v-for="(group, gi) in plan.groups"
      :key="gi"
      class="deck-mosaic-group"
      :style="{ flex: `${groupWeight(group)} 1 0px`, gap: `${props.gap}px` }"
    >
      <figure
        v-for="i in group"
        :key="i"
        class="deck-mosaic-item"
        :style="{ flex: `${itemWeight(group, i)} 1 0px` }"
      >
        <img
          :src="resolveAssetUrl(items[i].src)"
          :style="{ objectPosition: items[i].position || 'center' }"
          alt=""
          @load="onLoad(i, $event)"
        >
        <PhotoChip
          v-if="items[i].label || items[i].stop"
          class="deck-mosaic-chip"
          size="sm"
          :label="items[i].label"
          :stop="items[i].stop"
        />
      </figure>
    </div>
  </div>
</template>
