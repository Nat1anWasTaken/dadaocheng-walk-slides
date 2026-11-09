<script setup lang="ts">
import { computed, useSlots } from 'vue'
import PhotoChip from '../components/PhotoChip.vue'
import { hasSlotContent, resolveAssetUrl } from '../layoutHelper'

const props = withDefaults(defineProps<{
  /** Book quote, about 30 characters at most. Corner brackets are added for you. */
  quote: string
  /** Attribution line under the quote */
  source?: string
  /** Present-day photo */
  image: string
  /** Focal point for cropping (CSS object-position) */
  position?: string
  /** Place name shown on the photo chip, e.g. "03 永樂市場" (leading stop number is dropped) */
  label?: string
  stop?: string | number
  /** Chip on the quote side */
  bookLabel?: string
  /** Chip on the photo side; `date` is appended */
  nowLabel?: string
  date?: string
  /** Optional one-line caption on the photo */
  caption?: string
  /** Set the quote vertically (直排), for quotes up to about 24 characters */
  vertical?: boolean
  /** Photo on the left, quote on the right */
  reverse?: boolean
}>(), {
  source: '洪愛珠《老派少女購物路線》',
  position: 'center',
  bookLabel: '書中',
  nowLabel: '現場',
  date: '2026.10.26',
  vertical: false,
  reverse: false,
})

const src = computed(() => resolveAssetUrl(props.image))
const slots = useSlots()
const hasNote = computed(() => hasSlotContent(slots.default))

// Strip brackets the author typed; the layout draws its own (hanging) ones.
const body = computed(() => String(props.quote ?? '').trim().replace(/^[「『“"]+/, '').replace(/[」』”"]+$/, ''))

// One size for every book quote so the comparison slides read as a set.
const sizeClass = computed(() => 'q-m')
</script>

<template>
  <div class="slidev-layout book-vs-now" :class="{ reverse: props.reverse, vertical: props.vertical }">
    <div class="bvn-text">
      <blockquote class="bvn-quote" :class="sizeClass">
        <span class="bvn-open" aria-hidden="true">「</span>{{ body }}<span class="bvn-close" aria-hidden="true">」</span>
      </blockquote>
      <div class="bvn-source">
        {{ props.source }}
      </div>
      <div v-if="hasNote" class="bvn-note">
        <slot />
      </div>
    </div>
    <figure class="bvn-photo">
      <img :src="src" :style="{ objectPosition: props.position }" alt="">
      <PhotoChip class="bvn-chip-now" :label="props.label ? props.label.replace(/^\d+\s*/, '') : [props.nowLabel, props.date].filter(Boolean).join(' ')" dot="blue" />
      <figcaption v-if="props.caption">
        {{ props.caption }}
      </figcaption>
    </figure>
  </div>
</template>
