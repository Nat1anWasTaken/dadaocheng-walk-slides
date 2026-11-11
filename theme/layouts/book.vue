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
  <div class="slidev-layout book" :class="{ 'is-quoting': hasQuote && $clicks >= 1 }">
    <div class="book-text">
      <slot />
    </div>
    <div class="book-stage">
      <img :src="src" alt="">
    </div>
    <!--
      `::quote::` takes over the whole page on the first click (set `clicks: 1`).
      The book drifts out of focus as the line it holds comes into focus.
    -->
    <Transition name="book-quote" :duration="{ enter: 1150, leave: 320 }">
      <div v-if="hasQuote && $clicks >= 1" class="slidev-layout quote book-quote">
        <span class="deck-quote-mark" aria-hidden="true">“</span>
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

.book-text,
.book-stage {
  transition:
    opacity 0.5s var(--deck-ease-out),
    filter 0.6s var(--deck-ease-out),
    scale 0.8s var(--deck-ease-out);
}

.book.is-quoting .book-text,
.book.is-quoting .book-stage {
  opacity: 0;
  filter: blur(10px);
  scale: 0.97;
}

.book.is-quoting .book-stage {
  scale: 1.04;
}

.book-quote {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: none;
}

.book-quote-enter-active .deck-quote-mark {
  transition:
    opacity 0.6s var(--deck-ease-out) 0.18s,
    scale 0.7s var(--deck-ease-out) 0.18s,
    translate 0.7s var(--deck-ease-out) 0.18s;
}

.book-quote-enter-active :deep(h1) {
  transition:
    opacity 0.85s var(--deck-ease-out) 0.3s,
    filter 0.85s var(--deck-ease-out) 0.3s;
}

.book-quote-enter-from .deck-quote-mark {
  opacity: 0;
  scale: 0.7;
  translate: 0 6px;
}

.book-quote-enter-from :deep(h1) {
  opacity: 0;
  filter: blur(8px);
}

.book-quote-leave-active {
  transition:
    opacity 0.3s var(--deck-ease-in),
    filter 0.3s var(--deck-ease-in);
}

.book-quote-leave-to {
  opacity: 0;
  filter: blur(6px);
}
</style>
