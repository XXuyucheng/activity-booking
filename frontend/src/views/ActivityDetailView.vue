<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import DateStrip from '../components/DateStrip.vue'
import BookingFormDialog, {
  type BookingPayload,
} from '../components/BookingFormDialog.vue'
import { createBooking } from '../api/bookings'
import { fetchActivity, type ActivityDetailResponse } from '../api/catalog'
import { ApiError, redirectToLogin } from '../api/http'
import { getMockExtrasByName } from '../data/mock-activities'
import { coverUrl } from '../lib/cover'
import {
  groupSchedules,
  isSessionFull,
  isSlotFull,
  slotRemaining,
  type DateSession,
  type ScheduleSlot,
} from '../lib/schedules'
import { useCampRouter } from '../lib/campRoute'

const route = useRoute()
const { campSlug, push, router } = useCampRouter()

const activity = ref<ActivityDetailResponse | null>(null)
const missing = ref(false)
const loading = ref(true)
const selectedDate = ref('')
const selectedTime = ref('')
const showBooking = ref(false)
const submitting = ref(false)

const extras = computed(() =>
  activity.value ? getMockExtrasByName(activity.value.name) : undefined,
)
const cover = computed(() =>
  activity.value ? coverUrl(activity.value.cover) : '',
)
const images = computed(() => extras.value?.images ?? [cover.value].filter(Boolean))
const intro = computed(
  () => extras.value?.intro ?? activity.value?.description ?? '',
)
const sessions = computed(() => {
  if (!activity.value) return []
  const now = Date.now()
  const upcoming = activity.value.schedules.filter(
    (item) => new Date(item.start_time).getTime() > now,
  )
  return groupSchedules(upcoming)
})
const price = computed(() => Number(activity.value?.price ?? 0))
const childPrice = computed(() => Number(activity.value?.child_price ?? 0))

const selectedSession = computed(
  () =>
    sessions.value.find((item) => item.date === selectedDate.value) ?? null,
)

const selectedSlot = computed(
  () =>
    selectedSession.value?.slots.find(
      (slot) => slot.time === selectedTime.value,
    ) ?? null,
)

const selectedLabel = computed(() => {
  const session = selectedSession.value
  if (!session) return '请选择场次'
  const slot = selectedSlot.value
  return slot ? `${formatSession(session)} · ${slot.time}` : formatSession(session)
})

const pickDefaultSlot = (session: DateSession | null) => {
  if (!session) return ''
  const open = session.slots.find((slot) => !isSlotFull(slot))
  return (open ?? session.slots[0])?.time ?? ''
}

const load = async () => {
  missing.value = false
  loading.value = true
  try {
    const detail = await fetchActivity(String(route.params.id))
    if (detail.camp_slug !== campSlug.value) {
      activity.value = null
      missing.value = true
      return
    }
    activity.value = detail
  } catch (error) {
    activity.value = null
    missing.value = true
    if (error instanceof ApiError && error.status !== 404) {
      showToast('活动加载失败')
    }
  } finally {
    loading.value = false
  }
}

watch(
  () => [route.params.id, campSlug.value],
  () => {
    void load()
  },
  { immediate: true },
)

watch(
  sessions,
  (list) => {
    const open = list.find((session) => !isSessionFull(session))
    selectedDate.value = (open ?? list[0])?.date ?? ''
  },
  { immediate: true },
)

watch(
  selectedSession,
  (session) => {
    selectedTime.value = pickDefaultSlot(session)
  },
  { immediate: true },
)

const formatSession = (session: DateSession) => {
  const [, month, day] = session.date.split('-')
  return `${Number(month)}月${Number(day)}日 ${session.weekday}`
}

const slotLabel = (slot: ScheduleSlot) =>
  isSlotFull(slot) ? '已满' : `余 ${slotRemaining(slot)}`

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void push('home')
}

const remainingCount = computed(() => {
  const slot = selectedSlot.value
  return slot ? Math.max(slotRemaining(slot), 0) : 0
})

const onBook = () => {
  const session = selectedSession.value
  if (!session) {
    showToast('请选择场次')
    return
  }
  const slot = selectedSlot.value
  if (!slot) {
    showToast('请选择时间段')
    return
  }
  if (isSlotFull(slot)) {
    showToast('名额已满')
    return
  }
  showBooking.value = true
}

const onBookingSubmit = async (payload: BookingPayload) => {
  const slot = selectedSlot.value
  if (!slot) return
  submitting.value = true
  try {
    await createBooking({
      schedule_id: slot.scheduleId,
      contact_name: payload.name,
      contact_phone: payload.phone,
      adult_count: payload.count,
      child_count: payload.childCount,
      remark: payload.remark,
    })
    showBooking.value = false
    try {
      await showConfirmDialog({
        className: 'ab-dialog',
        title: '预约成功',
        message: '已收到你的预约，我们会尽快确认',
        confirmButtonText: '查看我的预约',
        cancelButtonText: '继续逛逛',
      })
      void push('bookings')
    } catch {
      await load()
    }
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      redirectToLogin()
      return
    }
    if (error instanceof ApiError && error.status === 409) {
      showToast('名额不足')
      await load()
      return
    }
    showToast(error instanceof Error ? error.message : '预约失败')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div v-if="loading" class="ab-page missing">
    <van-nav-bar
      title="活动详情"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />
    <p class="missing-copy">加载中…</p>
  </div>

  <div v-else-if="missing" class="ab-page missing">
    <van-nav-bar
      title="活动详情"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />
    <p class="missing-copy">活动不存在或已下架</p>
  </div>

  <div v-else-if="activity" class="page">
    <div class="hero">
      <van-swipe class="swipe" :loop="images.length > 1">
        <van-swipe-item v-for="(src, index) in images" :key="index">
          <img class="swipe-img" :src="src" :alt="activity.name" />
        </van-swipe-item>
        <template #indicator="{ active, total }">
          <div class="indicator">{{ active + 1 }}/{{ total }}</div>
        </template>
      </van-swipe>
      <div class="hero-nav">
        <van-nav-bar
          :title="activity.name"
          left-arrow
          safe-area-inset-top
          :border="false"
          @click-left="goBack"
        />
      </div>
    </div>

    <div class="body">
      <h1 class="ab-title title">{{ activity.name }}</h1>
      <p class="price">
        <span class="price-item">¥{{ activity.price }}<small>/成人</small></span>
        <span class="price-item">¥{{ activity.child_price }}<small>/儿童</small></span>
      </p>
      <p class="intro">{{ intro }}</p>
      <div v-if="extras?.tags.length" class="tags">
        <van-tag
          v-for="tag in extras.tags"
          :key="tag"
          plain
          type="primary"
        >
          {{ tag }}
        </van-tag>
      </div>
      <h2 class="ab-title dates-title">选择场次</h2>
      <DateStrip v-model="selectedDate" :sessions="sessions" />
      <div v-if="selectedSession" class="slots" role="list">
        <button
          v-for="slot in selectedSession.slots"
          :key="slot.scheduleId"
          type="button"
          class="slot"
          :class="{
            'slot--active': slot.time === selectedTime,
            'slot--full': isSlotFull(slot),
          }"
          @click="selectedTime = slot.time"
        >
          <span class="slot-time">{{ slot.time }}</span>
          <span class="slot-left">{{ slotLabel(slot) }}</span>
        </button>
      </div>

      <section class="detail">
        <h2 class="ab-title detail-title">活动详情</h2>
        <ul v-if="extras?.highlights.length" class="highlights">
          <li v-for="item in extras.highlights" :key="item">{{ item }}</li>
        </ul>
        <template v-if="extras">
          <div
            v-for="section in extras.detail"
            :key="section.heading"
            class="detail-section"
          >
            <h3 class="detail-heading">{{ section.heading }}</h3>
            <p class="detail-body">{{ section.body }}</p>
          </div>
        </template>
        <p v-else class="detail-body">{{ activity.description }}</p>
        <img class="detail-img" :src="cover" :alt="activity.name" />
      </section>
    </div>

    <footer class="bar">
      <div class="bar-info">
        <p class="bar-price">¥{{ activity.price }}<small>起/人</small></p>
        <p class="picked">{{ selectedLabel }}</p>
      </div>
      <van-button class="book" type="primary" @click="onBook">
        立即预约
      </van-button>
    </footer>

    <BookingFormDialog
      v-model:show="showBooking"
      :session-label="selectedLabel"
      :max-count="remainingCount"
      :price="price"
      :child-price="childPrice"
      :notice="activity.notice"
      :activity-id="activity.id"
      :submitting="submitting"
      @submit="onBookingSubmit"
    />
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background: var(--color-bg);
}

.hero {
  position: relative;
}

.swipe {
  height: 56vw;
  max-height: 320px;
  min-height: 220px;
  background: var(--color-pine);
}

.swipe-img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.indicator {
  position: absolute;
  right: var(--space-md);
  bottom: var(--space-md);
  padding: 2px var(--space-xs);
  font-size: var(--font-size-sm);
  color: var(--color-on-primary);
  background: rgb(0 0 0 / 45%);
  border-radius: var(--radius-sm);
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
  flex: 1;
  padding: var(--space-md);
  padding-bottom: var(--space-lg);
  background: var(--color-surface);
}

.title {
  font-size: var(--font-size-xl);
}

.price {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-cinnabar);
}

.price small {
  font-size: var(--font-size-sm);
  font-weight: 400;
  color: var(--color-ink-muted);
}

.intro {
  margin: var(--space-sm) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
  margin-top: var(--space-sm);
}

.dates-title {
  margin: var(--space-lg) 0 var(--space-sm);
  font-size: var(--font-size-lg);
}

.slots {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  margin-top: var(--space-sm);
}

.slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xs) var(--space-sm);
  color: var(--color-ink);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
  font: inherit;
}

.slot--active {
  background: color-mix(in srgb, var(--color-pine) 12%, var(--color-surface));
  border-color: var(--color-pine);
}

.slot--full {
  opacity: 0.55;
}

.slot-time {
  font-size: var(--font-size-md);
  font-weight: 600;
}

.slot-left {
  margin-top: 2px;
  font-size: var(--font-size-xs);
  color: var(--color-pine);
}

.slot--full .slot-left {
  color: var(--color-cinnabar);
}

.detail {
  margin-top: var(--space-lg);
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-line);
}

.detail-title {
  font-size: var(--font-size-lg);
}

.highlights {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
  margin: var(--space-sm) 0 0;
  padding: 0;
  list-style: none;
}

.highlights li {
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-pine);
  background: color-mix(in srgb, var(--color-pine) 10%, var(--color-surface));
  border-radius: var(--radius-sm);
}

.detail-section {
  margin-top: var(--space-md);
}

.detail-heading {
  margin: 0;
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--color-ink);
}

.detail-body {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.detail-img {
  display: block;
  width: 100%;
  margin-top: var(--space-md);
  border-radius: var(--radius-md);
  object-fit: cover;
}

.bar {
  position: sticky;
  bottom: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-md);
  padding-bottom: calc(var(--space-sm) + var(--safe-bottom));
  background: var(--color-surface);
  border-top: 1px solid var(--color-line);
}

.bar-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.bar-price {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  line-height: var(--line-height-sm);
  color: var(--color-cinnabar);
}

.bar-price small {
  font-size: var(--font-size-xs);
  font-weight: 400;
  color: var(--color-ink-muted);
}

.picked {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.book {
  flex: 0 0 auto;
  min-width: 132px;
}

.missing-copy {
  margin: var(--space-xl) var(--space-md);
  color: var(--color-ink-muted);
}
</style>
