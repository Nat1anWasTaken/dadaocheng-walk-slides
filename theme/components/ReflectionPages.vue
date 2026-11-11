<script setup lang="ts">
/**
 * Pages of a long reflection, one per click: `<template #0>`, `<template #1>`, ...
 * Set `clicks` in the slide's frontmatter to the last page number.
 *
 * Used instead of <v-switch>: its TransitionGroup re-renders between a fragment and a
 * wrapper element once a transition has run, which remounts the pages, so the page
 * being turned away starts from the wrong place. The page turn itself is styled in
 * layouts/reflection.vue.
 */
import { useSlideContext } from '@slidev/client'
import { computed, useSlots } from 'vue'

const slots = useSlots()
const { $clicks } = useSlideContext()

const pages = computed(() => Object.keys(slots).filter(name => /^\d+$/.test(name)).map(Number).sort((a, b) => a - b))
// The last page whose number has been reached (export without clicks shows the last page)
const current = computed(() => pages.value.reduce((shown, n) => (n <= $clicks.value ? n : shown), pages.value[0] ?? 0))
</script>

<template>
  <Transition name="reflection-scroll">
    <div :key="current" class="reflection-page">
      <slot :name="String(current)" />
    </div>
  </Transition>
</template>
