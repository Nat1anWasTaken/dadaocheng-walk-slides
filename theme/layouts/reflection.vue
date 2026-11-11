<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

defineProps<{
  kicker?: string
}>()

// The rule follows the text's length, easing to it when a long reflection turns a page.
const content = ref<HTMLElement>()
const ruleHeight = ref<number>()
let ro: ResizeObserver | undefined
onMounted(() => {
  if (!content.value)
    return
  ro = new ResizeObserver(() => {
    const h = content.value?.offsetHeight
    // Hidden slides measure 0: keep the last length
    if (h)
      ruleHeight.value = h
  })
  ro.observe(content.value)
})
onBeforeUnmount(() => ro?.disconnect())
</script>

<template>
  <div class="slidev-layout reflection">
    <div class="reflection-header">
      <div v-if="kicker" class="google-kicker">
        {{ kicker }}
      </div>
      <slot name="name" />
    </div>
    <div class="reflection-body">
      <div class="reflection-rule" :style="ruleHeight ? { height: `${ruleHeight}px` } : undefined" aria-hidden="true" />
      <div class="reflection-viewport">
        <div ref="content" class="reflection-content">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reflection {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.reflection-header :deep(h1) {
  margin: 0.2rem 0 0;
  font-size: 2rem;
  line-height: 1.2;
}

.reflection-body {
  position: relative;
  flex: 1;
  min-height: 0;
  padding-left: 1.2rem;
}

.reflection-rule {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 3px;
  background: var(--google-blue);
  transition: height 0.75s var(--deck-ease-in-out);
}

.reflection-content {
  position: relative;
}

/*
 * Long reflections are split into pages with <ReflectionPages>.
 * A page turn reads as one column of text scrolling on: both pages move by the
 * column's height (100cqh), so they travel as one strip, and fade at its edges.
 * The viewport reaches into the gap above and the slide padding below, so the
 * fades never touch resting text.
 */
.reflection-viewport {
  container-type: size;
  height: calc(100% + 2.85rem);
  margin: -1.1rem 0 -1.75rem;
  padding: 1.1rem 0 1.75rem;
  overflow: clip;
  mask-image: linear-gradient(to bottom, transparent, #000 1.1rem, #000 calc(100% - 1.75rem), transparent);
}

.reflection-body :deep(.reflection-scroll-enter-active),
.reflection-body :deep(.reflection-scroll-leave-active) {
  transition: translate 0.8s var(--deck-ease-in-out);
}

.reflection-body :deep(.reflection-scroll-leave-active) {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
}

.reflection-body :deep(.reflection-scroll-enter-from) {
  translate: 0 100cqh;
}

.reflection-body :deep(.reflection-scroll-leave-to) {
  translate: 0 -100cqh;
}

/* Clicking back scrolls the other way: see motion.css */

.reflection-body :deep(.pending) {
  color: var(--google-muted);
  font-family: inherit;
}
</style>
