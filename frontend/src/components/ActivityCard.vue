<script setup lang="ts">
import { computed } from 'vue'

export type ActivityCardItem = {
  id: string
  name: string
  cover: string
  price: string | number
  status: 'open' | 'full'
}

const props = defineProps<{
  activity: ActivityCardItem
}>()

const emit = defineEmits<{
  select: [activity: ActivityCardItem]
}>()

const statusLabel = computed(() =>
  props.activity.status === 'full' ? '已满' : '可预约',
)

const statusType = computed(() =>
  props.activity.status === 'full' ? 'danger' : 'primary',
)

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
      <h2 class="ab-title title">{{ activity.name }}</h2>
      <div class="meta">
        <p class="price">¥{{ activity.price }}<small>/人起</small></p>
        <van-tag :type="statusType">
          {{ statusLabel }}
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

.title {
  margin-bottom: var(--space-sm);
  font-size: var(--font-size-lg);
  color: #fff;
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
