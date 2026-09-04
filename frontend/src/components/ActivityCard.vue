<script setup lang="ts">
import { computed } from 'vue'
import {
  activityBooked,
  activityCapacity,
  activityStatus,
  nextOpenSession,
  type Activity,
  type ActivityStatus,
} from '../data/mock-activities'

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

const status = computed(() => activityStatus(props.activity))

const slotsPreview = computed(() => {
  const session = nextOpenSession(props.activity)
  if (!session) return '全部时段已满'
  const [, month, day] = session.date.split('-')
  const times = session.slots
    .slice(0, 3)
    .map((slot) => slot.time.split('–')[0])
    .join(' / ')
  return `${Number(month)}/${day} ${session.weekday} · ${times}`
})

const onClick = () => {
  emit('select', props.activity)
}
</script>

<template>
  <article
    class="card"
    :class="{ 'card--full': status === 'full' }"
    role="button"
    tabindex="0"
    @click="onClick"
    @keydown.enter="onClick"
  >
    <img class="cover" :src="activity.cover" alt="" />
    <div class="copy">
      <h2 class="ab-title title">{{ activity.title }}</h2>
      <p class="session">{{ slotsPreview }}</p>
      <div class="meta">
        <p class="spots">
          名额 {{ activityBooked(activity) }} / {{ activityCapacity(activity) }}
        </p>
        <p class="price">¥{{ activity.price }}<small>/人起</small></p>
        <van-tag :type="statusType[status]">
          {{ statusLabel[status] }}
        </van-tag>
      </div>
    </div>
    <span class="hint">查看详情</span>
  </article>
</template>

<style scoped>
.card {
  position: relative;
  overflow: hidden;
  aspect-ratio: 1024 / 361;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 16px rgb(43 42 39 / 10%);
  transition: transform 0.15s ease;
}

.card:active {
  transform: scale(0.98);
}

.card--full {
  opacity: 0.30;
}

.cover {
  position: absolute;
  inset: 0;
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
    to top,
    rgb(0 0 0 / 85%),
    rgb(0 0 0 / 35%) 55%,
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

.price {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  line-height: var(--line-height-sm);
  color: #e8a87c;
}

.price small {
  font-size: var(--font-size-xs);
  font-weight: 400;
  opacity: 0.85;
}

.hint {
  position: absolute;
  right: var(--space-sm);
  bottom: var(--space-sm);
  z-index: 1;
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-on-primary);
  background: rgb(43 42 39 / 42%);
  border: 1px solid rgb(250 246 239 / 28%);
  border-radius: var(--radius-md);
  box-shadow: 0 6px 16px rgb(0 0 0 / 20%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  pointer-events: none;
}
</style>
