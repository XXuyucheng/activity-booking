<script setup lang="ts">
import type { Activity, ActivityStatus } from '../data/mock-activities'

const props = defineProps<{
  activity: Activity
}>()

const emit = defineEmits<{
  select: [activity: Activity]
}>()

const statusLabel: Record<ActivityStatus, string> = {
  open: '可预约',
  ongoing: '进行中',
  full: '已满',
}

const statusType: Record<ActivityStatus, 'primary' | 'success' | 'danger'> = {
  open: 'primary',
  ongoing: 'success',
  full: 'danger',
}

const onClick = () => {
  emit('select', props.activity)
}
</script>

<template>
  <article
    class="card"
    :class="{ 'card--full': activity.status === 'full' }"
    role="button"
    tabindex="0"
    @click="onClick"
    @keydown.enter="onClick"
  >
    <img class="cover" :src="activity.cover" alt="" />
    <div class="copy">
      <div class="row">
        <h2 class="ab-title title">{{ activity.title }}</h2>
        <van-tag :type="statusType[activity.status]">
          {{ statusLabel[activity.status] }}
        </van-tag>
      </div>
      <p class="session">{{ activity.session }}</p>
      <p class="spots">名额 {{ activity.booked }} / {{ activity.capacity }}</p>
    </div>
  </article>
</template>

<style scoped>
.card {
  position: relative;
  overflow: hidden;
  aspect-ratio: 1024 / 361;
  border-radius: var(--radius-md);
}

.card--full {
  opacity: 0.72;
}

.cover {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.copy {
  position: absolute;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 50%;
  height: 50%;
  padding: var(--space-sm) var(--space-md);
  background: linear-gradient(
    to right,
    rgb(0 0 0 / 0%),
    rgb(0 0 0 / 30%)
  );
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}

.title,
.session,
.spots {
  color: #fff;
}

.title {
  font-size: var(--font-size-lg);
}

.session,
.spots {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
}
</style>
