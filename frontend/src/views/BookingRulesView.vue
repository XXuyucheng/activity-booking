<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { bookingRules, getActivityById } from '../data/mock-activities'

const route = useRoute()
const router = useRouter()

const activity = computed(() => {
  const id = String(route.query.activityId ?? '')
  return id ? getActivityById(id) : undefined
})

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void router.push({ name: 'home' })
}
</script>

<template>
  <div class="ab-page">
    <van-nav-bar
      title="预约须知"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />

    <div class="page-body">
      <section v-if="activity" class="card notice-card">
        <h2 class="ab-title heading">本活动提示</h2>
        <p class="body">{{ activity.notice }}</p>
      </section>

      <section
        v-for="section in bookingRules"
        :key="section.heading"
        class="card"
      >
        <h2 class="ab-title heading">{{ section.heading }}</h2>
        <p class="body">{{ section.body }}</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.page-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-md);
}

.card {
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.heading {
  font-size: var(--font-size-lg);
}

.body {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.notice-card .heading {
  color: var(--color-pine);
}
</style>
