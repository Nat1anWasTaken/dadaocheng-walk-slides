<script setup lang="ts">
import { computed } from 'vue'

type Dot = 'blue' | 'red' | 'yellow' | 'green'

const props = withDefaults(defineProps<{
  /** Text of the chip. A leading stop number ("03 永樂市場") becomes a badge. */
  label?: string
  /** Explicit stop number badge; overrides a number parsed from `label`. */
  stop?: string | number
  /** Small colored dot instead of a number badge (matches the cover topics). */
  dot?: Dot
  size?: 'sm' | 'md'
}>(), {
  size: 'md',
})

const parts = computed(() => {
  const raw = (props.label ?? '').trim()
  const m = raw.match(/^(\d{1,2})\s+(.+)$/)
  const stop = props.stop != null && props.stop !== '' ? String(props.stop) : m?.[1]
  const text = props.stop == null && m ? m[2] : raw
  return { stop: stop ? stop.padStart(2, '0') : undefined, text }
})
</script>

<template>
  <span class="deck-chip" :class="`deck-chip-${props.size}`">
    <b v-if="parts.stop" class="deck-chip-stop">{{ parts.stop }}</b>
    <i v-else-if="props.dot" class="deck-chip-dot" :class="props.dot" />
    <span v-if="parts.text" class="deck-chip-text">{{ parts.text }}</span>
  </span>
</template>
