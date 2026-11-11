<script setup lang="ts">
import { computed, useSlots } from 'vue'
import { hasSlotContent, resolveAssetUrl } from '../layoutHelper'

const props = defineProps<{
  /** Book product shot (already 3D, on a white background) */
  image: string
}>()

const src = computed(() => resolveAssetUrl(props.image))
const slots = useSlots()
const hasQuote = computed(() => hasSlotContent(slots.quote))
</script>

<template>
  <div class="slidev-layout book">
    <div class="book-text">
      <slot />
    </div>
    <div class="book-stage">
      <img :src="src" alt="">
    </div>
    <!-- `::quote::` takes over the whole page on the first click (set `clicks: 1`) -->
    <Transition name="book-quote">
      <div v-if="hasQuote && $clicks >= 1" class="slidev-layout quote book-quote">
        <div class="google-layout-inner">
          <slot name="quote" />
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.slidev-layout.book {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: center;
  height: 100%;
  padding-right: 3.6rem;
  padding-left: 4.4rem;
}

.book-text :deep(h1) {
  font-family: var(--deck-font-serif);
  font-size: 44px;
  font-weight: 500;
  line-height: 1.25;
  /* Hang the opening 《 so the title lines up with the byline */
  margin-left: -0.5em;
}

.book-stage {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 0;
  padding: 2rem 0;
}

.book-stage img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.book-quote {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: white;
}

.book-quote-enter-active,
.book-quote-leave-active {
  transition: opacity 0.4s ease;
}

.book-quote-enter-from,
.book-quote-leave-to {
  opacity: 0;
}
</style>
