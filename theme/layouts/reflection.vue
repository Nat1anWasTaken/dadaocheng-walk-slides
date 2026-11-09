<script setup lang="ts">
defineProps<{
  kicker?: string
}>()
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
      <slot />
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
  min-height: 0;
  padding-left: 1.2rem;
  border-left: 3px solid var(--google-blue);
}

.reflection-body :deep(p) {
  margin: 0 0 0.75em;
  font-family: 'Noto Serif TC Deck', 'Noto Serif TC', serif;
  font-size: 18px;
  line-height: 1.8;
  text-align: justify;
  color: var(--google-ink);
}

.reflection-body :deep(p:last-child) {
  margin-bottom: 0;
}

/* Long reflections: tighten so they fit one slide */
.reflection.dense .reflection-body :deep(p) {
  font-size: 16px;
  line-height: 1.7;
  margin-bottom: 0.5em;
}

.reflection.roomy .reflection-body :deep(p) {
  font-size: 24px;
  line-height: 1.9;
}

.reflection-body :deep(.pending) {
  color: var(--google-muted);
  font-family: inherit;
}
</style>
