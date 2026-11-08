<script setup lang="ts">
import type { MosaicPhoto } from '../layoutHelper'
import { computed, useSlots } from 'vue'
import PhotoMosaic from '../components/PhotoMosaic.vue'
import { hasSlotContent } from '../layoutHelper'

const props = withDefaults(defineProps<{
  /** 2-4 photos: paths or { src, label, stop, position, ratio } */
  photos: (MosaicPhoto | string)[]
  kicker?: string
  gap?: number
  split?: number[]
  direction?: 'rows' | 'cols'
}>(), {})

const slots = useSlots()

// A heading in the slide body switches from full-bleed to a padded slide with a title.
const hasHeader = computed(() => Boolean(props.kicker) || hasSlotContent(slots.default))
</script>

<template>
  <div class="slidev-layout mosaic" :class="{ 'has-header': hasHeader }">
    <div v-if="hasHeader" class="google-layout-header">
      <div v-if="props.kicker" class="google-kicker">
        {{ props.kicker }}
      </div>
      <slot />
    </div>
    <PhotoMosaic
      class="mosaic-grid"
      :photos="props.photos"
      :gap="props.gap ?? (hasHeader ? 10 : 6)"
      :radius="hasHeader ? 12 : 0"
      :split="props.split"
      :direction="props.direction"
    />
  </div>
</template>
