<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPackById } from '../data/mock-activities'

const route = useRoute()
const router = useRouter()

const pack = computed(() => getPackById(String(route.params.id)))

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void router.push({ name: 'camp' })
}

const goCamp = () => {
  void router.push({ name: 'camp' })
}

const goHome = () => {
  void router.push({ name: 'home' })
}
</script>

<template>
  <div v-if="!pack" class="ab-page">
    <van-nav-bar
      title="套票详情"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />
    <p class="missing">套票不存在</p>
  </div>

  <div v-else class="ab-page page">
    <van-nav-bar
      :title="pack.name"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />

    <div class="page-body">
      <section class="card">
        <p class="price">
          ¥{{ pack.price }}<small>{{ pack.unit }}</small>
        </p>
        <p class="summary">{{ pack.summary }}</p>
      </section>

      <section class="card">
        <h2 class="ab-title heading">包含项目</h2>
        <ul class="includes">
          <li v-for="item in pack.includes" :key="item" class="include">
            <van-icon name="success" class="include-icon" />
            <span>{{ item }}</span>
          </li>
        </ul>
      </section>

      <section class="card">
        <h2 class="ab-title heading">说明</h2>
        <p class="notes">{{ pack.notes }}</p>
      </section>
    </div>

    <footer class="bar">
      <van-button class="bar-back" @click="goCamp">返回营地</van-button>
      <van-button type="primary" class="bar-book" @click="goHome">
        去预约活动
      </van-button>
    </footer>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}

.page-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-md);
  padding-bottom: var(--space-lg);
}

.card {
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.price {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  line-height: var(--line-height-sm);
  color: var(--color-cinnabar);
}

.price small {
  margin-left: 2px;
  font-size: var(--font-size-sm);
  font-weight: 400;
  color: var(--color-ink-muted);
}

.summary {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.heading {
  font-size: var(--font-size-lg);
}

.includes {
  margin: var(--space-sm) 0 0;
  padding: 0;
  list-style: none;
}

.include {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) 0;
  font-size: var(--font-size-md);
  color: var(--color-ink);
}

.include + .include {
  border-top: 1px solid var(--color-line);
}

.include-icon {
  color: var(--color-pine);
}

.notes {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.bar {
  position: sticky;
  bottom: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  padding-bottom: calc(var(--space-sm) + var(--safe-bottom));
  background: var(--color-surface);
  border-top: 1px solid var(--color-line);
}

.bar-back {
  flex: 1;
  color: var(--color-ink);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
}

.bar-book {
  flex: 1;
}

.missing {
  margin: var(--space-xl) var(--space-md);
  color: var(--color-ink-muted);
}
</style>
