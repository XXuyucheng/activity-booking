<script setup lang="ts">
import { showToast } from 'vant'
import CampHeader from '../components/CampHeader.vue'
import ActivityCard from '../components/ActivityCard.vue'
import { activities, camp, type Activity } from '../data/mock-activities'

const onSelect = (activity: Activity) => {
  if (activity.status === 'full') {
    showToast('名额已满')
    return
  }
  showToast('详情页将在下一步加入')
}
</script>

<template>
  <div class="ab-page">
    <div class="hero">
      <CampHeader :camp="camp" />
      <div class="hero-nav">
        <van-nav-bar
          title="营地活动预约"
          safe-area-inset-top
          :border="false"
        />
      </div>
    </div>
    <div class="page-body">
      <h2 class="ab-title list-title">本期活动</h2>
      <div class="list">
        <ActivityCard
          v-for="item in activities"
          :key="item.id"
          :activity="item"
          @select="onSelect"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero {
  position: relative;
}

.hero-nav {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  z-index: 2;
  background: linear-gradient(
    to bottom,
    rgb(0 0 0 / 20%),
    rgb(0 0 0 / 0%)
  );
}

.hero-nav :deep(.van-nav-bar) {
  --van-nav-bar-background: transparent;
  --van-nav-bar-title-text-color: var(--color-on-primary);
}

.page-body {
  padding: var(--space-md);
}

.list-title {
  margin: 0 0 var(--space-sm);
  font-size: var(--font-size-lg);
}

.list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
</style>
