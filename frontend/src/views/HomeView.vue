<script setup lang="ts">
import { useRouter } from 'vue-router'
import CampHeader from '../components/CampHeader.vue'
import ActivityCard from '../components/ActivityCard.vue'
import { activities, camp, type Activity } from '../data/mock-activities'

const router = useRouter()

const onSelect = (activity: Activity) => {
  void router.push({ name: 'activity', params: { id: activity.id } })
}

const goBookings = () => {
  void router.push({ name: 'bookings' })
}

const goCamp = () => {
  void router.push({ name: 'camp' })
}
</script>

<template>
  <div class="ab-page">
    <div class="hero">
      <CampHeader :camp="camp" @select="goCamp" />
      <div class="hero-nav">
        <van-nav-bar
          safe-area-inset-top
          :border="false"
          @click-right="goBookings"
        >
          <template #right>
            <span class="nav-right">我的预约</span>
          </template>
        </van-nav-bar>
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

.nav-right {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-on-primary);
}

.page-body {
  position: relative;
  z-index: 1;
  margin-top: -24px;
  padding: var(--space-lg) var(--space-md) var(--space-md);
  background: var(--color-bg);
  border-radius: 16px 16px 0 0;
  box-shadow: 0 -8px 24px rgb(43 42 39 / 10%);
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
