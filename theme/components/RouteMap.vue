<script setup lang="ts">
/**
 * Walk map drawn from OpenStreetMap street lines (theme/data/dadaocheng-streets.json)
 * and the route stops/path in data/route.json. See DESIGN notes in the repo for props.
 */
import { onSlideEnter, onSlideLeave, useNav, useSlideContext } from '@slidev/client'
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import defaultRoute from '../../data/route.json'
import streets from '../data/dadaocheng-streets.json'

type Side = 'left' | 'right' | 'top' | 'bottom'

interface Stop {
  id: string
  slug?: string
  name_zh: string
  short?: string
  lat: number
  lon: number
  label?: Side
}

interface RouteData {
  view?: number[]
  stops: Stop[]
  path?: number[][]
}

const props = withDefaults(defineProps<{
  /** Highlighted stop: 1-based number (3) or id ('03'). 0 / unset = whole route, no highlight. */
  active?: number | string
  /** Override data/route.json */
  route?: RouteData
  /** View [south, west, north, east]; always fully visible, extra space shows more streets. */
  bounds?: number[]
  /** Stop name pills: all, only the active one, or none. Default: all (compact: active). */
  labels?: 'all' | 'active' | 'none'
  /** Street names. Default: on (compact: off). */
  streetLabels?: boolean
  /** Animate the walked line when the slide is entered and when `active` changes. */
  draw?: boolean
  /** Small inset style: thinner streets, smaller markers, short attribution. */
  compact?: boolean
  /** Draw-on duration in ms */
  duration?: number
}>(), {
  labels: undefined,
  streetLabels: undefined,
  draw: false,
  compact: false,
  duration: 1400,
})

const data = computed<RouteData>(() => props.route ?? (defaultRoute as RouteData))
const stops = computed(() => data.value.stops ?? [])

// ---------------------------------------------------------------- projection
const view = computed(() => {
  let b = props.bounds ?? (props.compact ? undefined : data.value.view)
  if (!b && stops.value.length) {
    const lats = stops.value.map(s => s.lat)
    const lons = stops.value.map(s => s.lon)
    const pad = 0.00025
    b = [Math.min(...lats) - pad, Math.min(...lons) - pad, Math.max(...lats) + pad, Math.max(...lons) + pad]
  }
  b = b ?? streets.bounds
  const [s, w, n, e] = b.map(Number)
  return { s, w, n, e }
})
const LAT0 = 25.055
const KX = 111320 * Math.cos(LAT0 * Math.PI / 180)
const KY = 110574
const LON0 = 121.5105
const px = (lon: number) => (lon - LON0) * KX
const py = (lat: number) => (LAT0 - lat) * KY

const box = computed(() => {
  const x = px(view.value.w)
  const y = py(view.value.n)
  return { x, y, w: px(view.value.e) - x, h: py(view.value.s) - y }
})
const viewBox = computed(() => `${box.value.x} ${box.value.y} ${box.value.w} ${box.value.h}`)

// px per metre, from the rendered size (preserveAspectRatio meet)
const root = ref<HTMLElement>()
const size = reactive({ w: 800, h: 450 })
let ro: ResizeObserver | undefined
onMounted(() => {
  const measure = () => {
    if (root.value && root.value.clientWidth > 0 && root.value.clientHeight > 0) {
      size.w = root.value.clientWidth
      size.h = root.value.clientHeight
    }
  }
  measure()
  if (root.value) {
    ro = new ResizeObserver(measure)
    ro.observe(root.value)
  }
})
onBeforeUnmount(() => ro?.disconnect())

const k = computed(() => Math.min(size.w / box.value.w, size.h / box.value.h))
/** screen px -> map units (metres) */
const u = (n: number) => n / k.value
const sc = computed(() => (props.compact ? 0.62 : 1))

function line(pts: number[][]) {
  return pts.map(([lat, lon], i) => `${i ? 'L' : 'M'}${px(lon).toFixed(1)} ${py(lat).toFixed(1)}`).join('')
}

const streetPaths = computed(() => streets.streets.map(s => ({ rank: s.rank, d: line(s.pts) })))
const areaPaths = computed(() => streets.areas.map(a => ({ kind: a.kind, d: `${line(a.pts)}Z` })))
const WIDTH: Record<number, number> = { 1: 12, 2: 7.5, 3: 3.5 }

const showStreetLabels = computed(() => props.streetLabels ?? !props.compact)
const streetLabels = computed(() => streets.labels.map((l: any) => ({
  ...l,
  x: px(l.lon),
  y: py(l.lat),
})))

// ---------------------------------------------------------------- route
const routePts = computed(() => {
  const p = data.value.path?.length ? data.value.path : stops.value.map(s => [s.lat, s.lon])
  return p.map(([lat, lon]) => [px(lon), py(lat)] as [number, number])
})
const routeD = computed(() => routePts.value.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(''))

const cumulative = computed(() => {
  const pts = routePts.value
  const acc = [0]
  for (let i = 1; i < pts.length; i++)
    acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
  return acc
})

/** Fraction of the path at which each stop is reached (path may retrace streets). */
const stopFractions = computed(() => {
  const pts = routePts.value
  const acc = cumulative.value
  const total = acc[acc.length - 1] || 1
  let from = 0
  return stops.value.map((s) => {
    const sx = px(s.lon)
    const sy = py(s.lat)
    const d = pts.map(([x, y]) => Math.hypot(x - sx, y - sy))
    let best = Infinity
    for (let j = from; j < pts.length; j++) best = Math.min(best, d[j])
    let j = from
    while (j < pts.length - 1 && d[j] > best + 2) j++
    from = j
    return acc[j] / total
  })
})

const activeIndex = computed(() => {
  const a = props.active
  if (a == null || a === '' || a === 0 || a === '0')
    return -1
  const key = String(a)
  return stops.value.findIndex(s => s.id === key || s.id === key.padStart(2, '0') || s.slug === key)
})

const target = computed(() => (activeIndex.value >= 0 ? stopFractions.value[activeIndex.value] : 1))

// ---------------------------------------------------------------- draw-on
const { $renderContext } = useSlideContext()
const { isPrintMode } = useNav()
const live = computed(() => ['slide', 'presenter'].includes($renderContext.value) && !isPrintMode.value)
const entered = ref(!props.draw)

if (props.draw) {
  onSlideEnter(() => {
    if (!live.value) {
      entered.value = true
      return
    }
    entered.value = false
    requestAnimationFrame(() => requestAnimationFrame(() => (entered.value = true)))
  })
  onSlideLeave(() => {
    if (live.value)
      entered.value = false
  })
}

const shown = computed(() => (props.draw && live.value && !entered.value ? 0 : target.value))
const walkedStyle = computed(() => ({
  strokeDashoffset: String(1 - shown.value),
  opacity: shown.value > 0.001 ? 1 : 0,
  transition: live.value ? `stroke-dashoffset ${props.duration}ms cubic-bezier(.4,0,.2,1)` : 'none',
}))

// ---------------------------------------------------------------- markers & labels
const labelMode = computed(() => props.labels ?? (props.compact ? 'none' : 'all'))

function textWidth(t: string, fs: number) {
  let w = 0
  for (const ch of t) w += ch.charCodeAt(0) > 0x2E80 ? fs : fs * 0.58
  return w
}

const markers = computed(() => stops.value.map((s, i) => {
  const state = activeIndex.value < 0 || i < activeIndex.value ? 'done' : i === activeIndex.value ? 'active' : 'todo'
  const r = (state === 'active' ? 14 : 11.5) * sc.value
  const text = s.short ?? s.name_zh
  const fs = 13.5 * sc.value
  const h = 24 * sc.value
  const w = textWidth(text, fs) + 18 * sc.value
  const gap = 5 * sc.value
  const side: Side = s.label ?? 'right'
  let lx = r + gap
  let ly = -h / 2
  if (side === 'left')
    lx = -(r + gap) - w
  if (side === 'top') {
    lx = -w / 2
    ly = -(r + gap) - h
  }
  if (side === 'bottom') {
    lx = -w / 2
    ly = r + gap
  }
  const showLabel = labelMode.value === 'all' || (labelMode.value === 'active' && state === 'active')
  return {
    key: s.id,
    num: String(Number(s.id) || i + 1),
    x: px(s.lon),
    y: py(s.lat),
    state,
    r,
    label: showLabel ? { text, x: lx, y: ly, w, h, fs } : undefined,
  }
}))

// Active marker drawn last so it sits on top
const orderedMarkers = computed(() => [...markers.value].sort((a, b) => (a.state === 'active' ? 1 : 0) - (b.state === 'active' ? 1 : 0)))

const scaleBar = computed(() => {
  for (const m of [20, 50, 100, 200, 500]) {
    if (m * k.value >= 56)
      return { m, w: m * k.value }
  }
  return { m: 500, w: 500 * k.value }
})
</script>

<template>
  <div ref="root" class="deck-map" :class="{ 'deck-map-compact': props.compact }">
    <svg :viewBox="viewBox" preserveAspectRatio="xMidYMid meet" role="img" aria-label="走讀路線地圖">
      <rect :x="box.x - 2000" :y="box.y - 2000" :width="box.w + 4000" :height="box.h + 4000" class="deck-map-land" />
      <path v-for="(a, i) in areaPaths" :key="`a${i}`" :d="a.d" :class="`deck-map-area deck-map-${a.kind}`" :stroke-width="u(1)" />
      <g class="deck-map-casing">
        <path v-for="(s, i) in streetPaths" :key="`c${i}`" :d="s.d" :stroke-width="u((WIDTH[s.rank] + 2) * sc)" />
      </g>
      <g class="deck-map-street">
        <path v-for="(s, i) in streetPaths" :key="`s${i}`" :d="s.d" :stroke-width="u(WIDTH[s.rank] * sc)" />
      </g>
      <g v-if="showStreetLabels" class="deck-map-street-labels">
        <text
          v-for="l in streetLabels"
          :key="l.text"
          :class="{ vertical: l.vertical, water: l.water }"
          :transform="`translate(${l.x} ${l.y}) scale(${u(1)}) rotate(${l.angle ?? 0})`"
        >{{ l.text }}</text>
      </g>

      <!-- route: remaining part (dotted), casing, walked part -->
      <path :d="routeD" class="deck-map-route-rest" :stroke-width="u(3.2 * sc)" :stroke-dasharray="`${u(0.1)} ${u(7 * sc)}`" />
      <path :d="routeD" class="deck-map-route-casing" pathLength="1" stroke-dasharray="1 1" :style="walkedStyle" :stroke-width="u(10 * sc)" />
      <path :d="routeD" class="deck-map-route" pathLength="1" stroke-dasharray="1 1" :style="walkedStyle" :stroke-width="u(5.5 * sc)" />

      <g
        v-for="m in orderedMarkers"
        :key="m.key"
        class="deck-map-stop"
        :class="`is-${m.state}`"
        :transform="`translate(${m.x} ${m.y}) scale(${u(1)})`"
      >
        <circle v-if="m.state === 'active'" class="deck-map-halo" :r="m.r * 1.9" />
        <circle class="deck-map-dot" :r="m.r" :stroke-width="2.5 * sc" />
        <text class="deck-map-num" :style="{ fontSize: `${(m.state === 'active' ? 13 : 11.5) * sc}px` }">{{ m.num }}</text>
        <g v-if="m.label" class="deck-map-label">
          <rect :x="m.label.x" :y="m.label.y" :width="m.label.w" :height="m.label.h" :rx="m.label.h / 2" />
          <text :x="m.label.x + m.label.w / 2" :y="m.label.y + m.label.h / 2" :style="{ fontSize: `${m.label.fs}px` }">{{ m.label.text }}</text>
        </g>
      </g>
    </svg>
    <div v-if="!props.compact" class="deck-map-scale">
      <i :style="{ width: `${scaleBar.w}px` }" />{{ scaleBar.m }} m
    </div>
    <div class="deck-map-credit">
      © OpenStreetMap contributors
    </div>
  </div>
</template>
