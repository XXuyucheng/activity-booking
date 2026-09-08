<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showImagePreview } from 'vant'
import ActivityCard, {
  type ActivityCardItem,
} from '../components/ActivityCard.vue'
import campPoster from '../assets/camp-poster.webp'
import campMap from '../assets/camp-ground.png'
import { fetchCamp, fetchCampActivities } from '../api/catalog'
import { camp as campMock, packLabel } from '../data/mock-activities'
import { coverUrl } from '../lib/cover'

const router = useRouter()
const camp = ref({ ...campMock })
const list = ref<ActivityCardItem[]>([])
const heroImages = [campPoster]

const previewMap = () => {
  showImagePreview({ images: [campMap], closeable: true })
}

const load = async () => {
  try {
    const [apiCamp, activities] = await Promise.all([
      fetchCamp(),
      fetchCampActivities(),
    ])
    camp.value = {
      ...campMock,
      name: apiCamp.name,
      intro: apiCamp.description || campMock.intro,
    }
    list.value = activities.map((item) => ({
      id: item.id,
      name: item.name,
      cover: coverUrl(item.cover),
      price: item.price,
      status: item.status,
    }))
  } catch {
    list.value = []
  }
}

onMounted(() => {
  void load()
})

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void router.push({ name: 'home' })
}

const goHome = () => {
  void router.push({ name: 'home' })
}

const onSelect = (activity: ActivityCardItem) => {
  void router.push({ name: 'activity', params: { id: activity.id } })
}

const goPack = (packId: string) => {
  void router.push({ name: 'pack', params: { id: packId } })
}
</script>

<template>
  <div class="ab-page">
    <div class="hero">
      <van-swipe class="hero-swipe" :loop="heroImages.length > 1">
        <van-swipe-item v-for="(src, index) in heroImages" :key="index">
          <img class="hero-img" :src="src" :alt="`${camp.name}海报`" />
        </van-swipe-item>
      </van-swipe>
      <div class="hero-nav">
        <van-nav-bar
          title="营地介绍"
          left-arrow
          safe-area-inset-top
          :border="false"
          @click-left="goBack"
        />
      </div>
    </div>

    <div class="body">
      <section class="card">
        <h1 class="ab-title name">{{ camp.name }}</h1>
        <p class="location">{{ camp.location }}</p>
        <p class="story">{{ camp.story }}</p>
        <div class="map" @click="previewMap">
          <img class="map-img" :src="campMap" alt="营地导览图" />
          <span class="map-hint">放大查看</span>
        </div>
      </section>

      <h2 class="ab-title section-title">营地项目</h2>
      <div class="card facilities">
        <div
          v-for="item in camp.facilities"
          :key="item.name"
          class="facility"
        >
          <div class="facility-head">
            <span class="facility-name">{{ item.name }}</span>
            <button
              v-if="item.packId"
              type="button"
              class="pack-tag"
              @click="goPack(item.packId)"
            >
              <van-tag plain type="primary">{{ packLabel(item.packId) }}</van-tag>
            </button>
            <van-tag v-else plain>{{ packLabel(null) }}</van-tag>
          </div>
          <p class="facility-desc">{{ item.desc }}</p>
        </div>
      </div>

      <h2 class="ab-title section-title">本期活动</h2>
      <div class="list">
        <ActivityCard
          v-for="item in list"
          :key="item.id"
          :activity="item"
          @select="onSelect"
        />
      </div>
    </div>

    <button type="button" class="fab" @click="goHome">
      <van-icon name="calendar-o" size="22" />
      <span class="fab-text">去预约</span>
    </button>
  </div>
</template>

<style scoped>
.hero {
  position: relative;
  height: 46vh;
  height: 46dvh;
  overflow: hidden;
  background: var(--color-pine);
}

.hero-swipe,
.hero-swipe :deep(.van-swipe__track),
.hero-swipe :deep(.van-swipe-item) {
  height: 100%;
}

.hero-img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.hero-nav {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  z-index: 2;
  background: linear-gradient(
    to bottom,
    rgb(0 0 0 / 80%),
    rgb(0 0 0 / 0%)
  );
}

.hero-nav :deep(.van-nav-bar) {
  --van-nav-bar-background: transparent;
  --van-nav-bar-title-text-color: var(--color-on-primary);
  --van-nav-bar-icon-color: var(--color-on-primary);
}

.body {
  position: relative;
  z-index: 1;
  margin-top: -24px;
  padding: var(--space-lg) var(--space-md) calc(var(--space-xl) + 64px);
  background: var(--color-bg);
  border-radius: 16px 16px 0 0;
  box-shadow: 0 -8px 24px rgb(43 42 39 / 10%);
}

.card {
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.name {
  font-size: var(--font-size-xl);
}

.location {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-pine);
}

.story {
  margin: var(--space-sm) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.map {
  position: relative;
  margin-top: var(--space-md);
  overflow: hidden;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
  cursor: zoom-in;
}

.map-img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.map-hint {
  position: absolute;
  right: var(--space-sm);
  bottom: var(--space-sm);
  padding: 2px var(--space-xs);
  font-size: var(--font-size-xs);
  color: var(--color-on-primary);
  background: rgb(43 42 39 / 42%);
  border-radius: var(--radius-sm);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  pointer-events: none;
}

.section-title {
  margin: var(--space-lg) 0 var(--space-sm);
  font-size: var(--font-size-lg);
}

.facilities {
  display: flex;
  flex-direction: column;
}

.facility {
  padding: var(--space-sm) 0;
}

.facility + .facility {
  border-top: 1px solid var(--color-line);
}

.facility-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}

.facility-name {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-ink);
}

.pack-tag {
  margin: 0;
  padding: 0;
  background: none;
  border: none;
}

.facility-desc {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  color: var(--color-ink-muted);
}

.list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.fab {
  position: fixed;
  right: var(--space-md);
  bottom: calc(var(--space-md) + var(--safe-bottom));
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  width: 60px;
  height: 60px;
  margin: 0;
  padding: 0;
  color: var(--color-on-primary);
  background: var(--color-pine);
  border: none;
  border-radius: 50%;
  box-shadow: 0 8px 20px rgb(47 93 74 / 35%);
}

.fab:active {
  transform: scale(0.94);
}

.fab-text {
  font-size: var(--font-size-xs);
}
</style>
