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
      <h2 class="ab-title title">{{ activity.title }}</h2>
      <p class="session">{{ activity.session }}</p>
      <div class="meta">
        <p class="spots">名额 {{ activity.booked }} / {{ activity.capacity }}</p>
        <van-tag :type="statusType[activity.status]">
          {{ statusLabel[activity.status] }}
        </van-tag>
      </div>
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
  opacity: 0.30;
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
  width: 100%;
  height: 100%;
  padding: var(--space-sm) var(--space-md);
  background: linear-gradient(
    to right,
    rgb(0 0 0 / 90%),
    rgb(0 0 0 / 0%)
  );
}

.meta {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-xs);
}

.title,
.session,
.spots {
  color: #fff;
}

.title {
  margin-bottom: var(--space-sm);
  font-size: var(--font-size-lg);
}

.session {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
}

.spots {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
}
</style>
