<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import CampHeader from '../components/CampHeader.vue'
import ActivityCard, {
  type ActivityCardItem,
} from '../components/ActivityCard.vue'
import { fetchCamp, fetchCampActivities } from '../api/catalog'
import { camp as campMock } from '../data/mock-activities'
import { coverUrl } from '../lib/cover'

const router = useRouter()
const headerCamp = ref({ ...campMock })
const list = ref<ActivityCardItem[]>([])
const loading = ref(true)
const error = ref('')

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const [camp, activities] = await Promise.all([
      fetchCamp(),
      fetchCampActivities(),
    ])
    headerCamp.value = {
      ...campMock,
      name: camp.name,
      intro: camp.description || campMock.intro,
    }
    list.value = activities.map((item) => ({
      id: item.id,
      name: item.name,
      cover: coverUrl(item.cover),
      price: item.price,
      status: item.status,
    }))
  } catch {
    error.value = '活动加载失败，请确认后端已启动'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void load()
})

const onSelect = (activity: ActivityCardItem) => {
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
      <CampHeader :camp="headerCamp" @select="goCamp" />
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
      <p v-if="loading" class="hint">加载中…</p>
      <p v-else-if="error" class="hint">{{ error }}</p>
      <div v-else class="list">
        <ActivityCard
          v-for="item in list"
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

.hint {
  margin: 0;
  font-size: var(--font-size-md);
  color: var(--color-ink-muted);
}

.list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
</style>
