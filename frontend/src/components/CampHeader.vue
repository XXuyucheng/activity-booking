<script setup lang="ts">
import type { Camp } from '../data/mock-activities'
import campPoster from '../assets/camp-poster.png'

defineProps<{
  camp: Camp
}>()
</script>

<template>
  <section class="camp">
    <div class="cover">
      <img :src="campPoster" :alt="`${camp.name}海报`" />
    </div>
    <div class="meta">
      <h1 class="ab-title name">{{ camp.name }}</h1>
      <p class="location">{{ camp.location }}</p>
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
  padding: var(--space-lg) var(--space-md) var(--space-md);
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

.location {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  opacity: 0.9;
}

.intro {
  margin: var(--space-sm) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  opacity: 0.92;
}
</style>
