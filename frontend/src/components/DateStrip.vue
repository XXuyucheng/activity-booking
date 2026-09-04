<script setup lang="ts">
import {
  isSessionFull,
  sessionBooked,
  sessionCapacity,
  type ActivitySession,
} from '../data/mock-activities'

defineProps<{
  sessions: ActivitySession[]
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [date: string]
}>()

const remaining = (item: ActivitySession) =>
  sessionCapacity(item) - sessionBooked(item)

const isFull = (item: ActivitySession) => isSessionFull(item)

const label = (item: ActivitySession) => {
  if (isSessionFull(item)) return '已满'
  return `余 ${remaining(item)}`
}

const monthDay = (date: string) => {
  const [, month, day] = date.split('-')
  return `${Number(month)}/${day}`
}

const onPick = (date: string) => {
  emit('update:modelValue', date)
}
</script>

<template>
  <div class="strip" role="list">
    <button
      v-for="item in sessions"
      :key="item.date"
      type="button"
      class="chip"
      :class="{
        'chip--active': item.date === modelValue,
        'chip--full': isFull(item),
      }"
      role="listitem"
      @click="onPick(item.date)"
    >
      <span class="chip-week">{{ item.weekday }}</span>
      <span class="chip-day">{{ monthDay(item.date) }}</span>
      <span class="chip-left">{{ label(item) }}</span>
    </button>
  </div>
</template>

<style scoped>
.strip {
  display: flex;
  gap: var(--space-sm);
  overflow-x: auto;
  padding-bottom: var(--space-xs);
  -webkit-overflow-scrolling: touch;
}

.chip {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 72px;
  padding: var(--space-sm) var(--space-xs);
  color: var(--color-ink);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
  font: inherit;
}

.chip--active {
  background: color-mix(in srgb, var(--color-pine) 12%, var(--color-surface));
  border-color: var(--color-pine);
}

.chip--full {
  opacity: 0.55;
}

.chip-week {
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.chip-day {
  margin-top: var(--space-xs);
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.chip-left {
  margin-top: var(--space-xs);
  font-size: var(--font-size-sm);
  color: var(--color-pine);
}

.chip--full .chip-left {
  color: var(--color-cinnabar);
}
</style>
