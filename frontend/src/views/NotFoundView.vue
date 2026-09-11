<script setup lang="ts">
import { DEFAULT_CAMP_SLUG } from '../lib/camp'
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  const slug = document.documentElement.dataset.camp || DEFAULT_CAMP_SLUG
  void router.push({ name: 'home', params: { campSlug: slug } })
}
</script>

<template>
  <div class="ab-page page">
    <div class="empty">
      <h1 class="ab-title title">页面不存在</h1>
      <p class="copy">链接可能写错了，或页面已经下线。</p>
      <van-button type="primary" @click="goHome">回首页</van-button>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100dvh;
  background: var(--color-bg);
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xl) var(--space-md);
  text-align: center;
}

.title {
  font-size: var(--font-size-xl);
}

.copy {
  margin: var(--space-sm) 0 var(--space-lg);
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}
</style>
