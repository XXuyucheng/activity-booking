<script setup lang="ts">
import type { Camp } from '../data/mock-activities'
import campPoster from '../assets/camp-poster.webp'

defineProps<{
  camp: Camp
}>()

const emit = defineEmits<{
  select: []
}>()

const onClick = () => {
  emit('select')
}
</script>

<template>
  <section
    class="camp"
    role="button"
    tabindex="0"
    @click="onClick"
    @keydown.enter="onClick"
  >
    <div class="cover">
      <img :src="campPoster" :alt="`${camp.name}海报`" />
    </div>
    <div class="meta">
      <h1 class="ab-title name">{{ camp.name }}</h1>
      <div class="meta-row">
        <p class="location">{{ camp.location }}</p>
        <span class="hint">营地介绍 ›</span>
      </div>
      <p class="intro">{{ camp.intro }}</p>
    </div>
  </section>
</template>

<style scoped>
.camp {
  position: relative;
  height: 75vh;
  height: 75dvh;
  overflow: hidden;
}

.cover {
  position: absolute;
  inset: 0;
  background: var(--color-pine);
}

.cover img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.meta {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: var(--space-lg) var(--space-md) calc(var(--space-md) + 24px);
  background: linear-gradient(
    to bottom,
    rgb(0 0 0 / 0%),
    rgb(0 0 0 / 80%)
  );
}

.name,
.location,
.intro {
  color: var(--color-on-primary);
}

.name {
  font-size: var(--font-size-xl);
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
  margin-top: var(--space-xs);
}

.location {
  margin: 0;
  font-size: var(--font-size-sm);
  opacity: 0.9;
}

.intro {
  margin: var(--space-sm) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  opacity: 0.92;
}

.hint {
  flex: 0 0 auto;
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-on-primary);
  background: rgb(43 42 39 / 42%);
  border: 1px solid rgb(250 246 239 / 28%);
  border-radius: var(--radius-md);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  pointer-events: none;
}
</style>
