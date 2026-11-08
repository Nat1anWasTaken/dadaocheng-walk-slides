<script setup lang="ts">
import { computed, useSlots } from 'vue'
import PhotoChip from '../components/PhotoChip.vue'
import RouteMap from '../components/RouteMap.vue'
import { hasSlotContent, resolveAssetUrl } from '../layoutHelper'

const props = withDefaults(defineProps<{
  /** Photo path, e.g. /images/03-yongle-market-1.jpg */
  image: string
  /** Focal point for cropping (CSS object-position), e.g. "50% 30%" */
  position?: string
  /** cover = fill the slide (crops); contain = whole photo over a blurred copy */
  fit?: 'cover' | 'contain'
  /** Chip in the top-left corner, e.g. "03 永樂市場" */
  label?: string
  stop?: string | number
  /** One line at the bottom */
  caption?: string
  /** Bottom scrim strength (only drawn when there is a caption) */
  scrim?: 'light' | 'strong' | 'none'
  /** Show a small RouteMap inset highlighting this stop (number or id) */
  map?: number | string
}>(), {
  position: 'center',
  fit: 'cover',
  scrim: 'light',
})

const src = computed(() => resolveAssetUrl(props.image))
const hasChip = computed(() => Boolean(props.label || props.stop))
const slots = useSlots()
const hasCaption = computed(() => Boolean(props.caption) || hasSlotContent(slots.default))
</script>

<template>
  <div class="slidev-layout photo" :class="[`fit-${props.fit}`, { 'has-map': props.map != null && props.map !== '' }]">
    <div v-if="props.fit === 'contain'" class="deck-photo-backdrop" :style="{ backgroundImage: `url(&quot;${src}&quot;)` }" />
    <img class="deck-photo-img" :src="src" :style="{ objectPosition: props.position }" alt="">
    <div v-if="hasCaption && props.scrim !== 'none'" class="deck-photo-scrim" :class="props.scrim" />
    <PhotoChip v-if="hasChip" class="deck-photo-chip" :label="props.label" :stop="props.stop" />
    <div v-if="hasCaption" class="deck-photo-caption">
      <p v-if="props.caption">
        {{ props.caption }}
      </p>
      <slot />
    </div>
    <div v-if="props.map != null && props.map !== ''" class="deck-photo-map">
      <RouteMap :active="props.map" compact />
    </div>
  </div>
</template>
