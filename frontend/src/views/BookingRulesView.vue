<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchActivity } from '../api/catalog'
import { bookingRules } from '../data/mock-activities'
import { useCampRouter } from '../lib/campRoute'

const route = useRoute()
const { campSlug, push, router } = useCampRouter()
const notice = ref('')

onMounted(() => {
  const id = String(route.query.activityId ?? '')
  if (!id) return
  void fetchActivity(id)
    .then((item) => {
      notice.value = item.camp_slug === campSlug.value ? item.notice : ''
    })
    .catch(() => {
      notice.value = ''
    })
})

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void push('home')
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
      <section v-if="notice" class="card notice-card">
        <h2 class="ab-title heading">本活动提示</h2>
        <p class="body">{{ notice }}</p>
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
