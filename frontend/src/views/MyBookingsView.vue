<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  fetchBookings,
  type BookingResponse,
} from '../api/bookings'
import { ApiError, redirectToLogin } from '../api/http'
import { coverUrl } from '../lib/cover'
import { formatClockRange } from '../lib/schedules'
import { getMockExtrasByName } from '../data/mock-activities'
import { PAYMENT_HINT, isPaidOff } from '../data/booking-copy'
import { useCampRouter } from '../lib/campRoute'

const { campSlug, push, router } = useCampRouter()
const list = ref<BookingResponse[]>([])
const loading = ref(true)

const statusLabel: Record<string, string> = {
  pending: '已预约待建联',
  contacted: '已建联',
  expired: '失效',
}

const statusType: Record<string, 'primary' | 'success' | 'default'> = {
  pending: 'primary',
  contacted: 'success',
  expired: 'default',
}

const load = async () => {
  loading.value = true
  try {
    list.value = await fetchBookings(campSlug.value)
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      redirectToLogin()
      return
    }
    list.value = []
  } finally {
    loading.value = false
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
  void push('home')
}

const goHome = () => {
  void push('home')
}

const openDetail = (id: string) => {
  void push('booking-detail', { id })
}

const coverOf = (item: BookingResponse) => {
  const extras = getMockExtrasByName(item.activity_name)
  return extras?.images[0] ?? coverUrl('')
}

const sessionOf = (item: BookingResponse) =>
  formatClockRange(item.start_time, item.end_time)
</script>

<template>
  <div class="ab-page">
    <van-nav-bar
      title="我的预约"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />

    <div class="page-body">
      <p v-if="loading" class="count">加载中…</p>
      <template v-else-if="list.length">
        <p class="count">共 {{ list.length }} 条</p>
        <div class="list">
          <article
            v-for="item in list"
            :key="item.id"
            class="card"
            role="button"
            tabindex="0"
            @click="openDetail(item.id)"
            @keydown.enter="openDetail(item.id)"
          >
            <img
              v-if="coverOf(item)"
              class="cover"
              :src="coverOf(item)"
              alt=""
            />
            <div class="card-body">
              <div class="card-head">
                <h2 class="ab-title card-title">{{ item.activity_name }}</h2>
                <van-tag :type="statusType[item.status] ?? 'default'">
                  {{ statusLabel[item.status] ?? item.status }}
                </van-tag>
                <span class="card-arrow">›</span>
              </div>
              <p class="card-session">{{ sessionOf(item) }}</p>
              <p class="card-meta">
                {{ item.contact_name }} · 成人 {{ item.adult_count }}
                <template v-if="item.child_count">· 儿童 {{ item.child_count }}</template>
                · {{ item.contact_phone }}
              </p>
              <p v-if="item.remark" class="card-remark">备注：{{ item.remark }}</p>
              <div class="card-totals">
                <p class="card-total">
                  合计 <span>¥{{ item.total_price }}</span>
                </p>
                <p class="card-total">
                  待付款 <span>¥{{ item.unpaid_amount }}</span>
                  <em v-if="isPaidOff(item.unpaid_amount)" class="paid-off">已付清</em>
                </p>
              </div>
              <p class="card-hint">{{ PAYMENT_HINT }}</p>
            </div>
          </article>
        </div>
      </template>

      <div v-else class="empty">
        <p class="empty-text">还没有预约</p>
        <van-button type="primary" @click="goHome">去逛逛</van-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-body {
  padding: var(--space-md);
}

.count {
  margin: 0 0 var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.list {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.cover {
  flex: 0 0 60px;
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--radius-md);
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}

.card-title {
  flex: 1;
  font-size: var(--font-size-lg);
}

.card-arrow {
  flex: 0 0 auto;
  font-size: var(--font-size-lg);
  color: var(--color-ink-muted);
}

.card-session {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-pine);
}

.card-meta {
  margin: var(--space-sm) 0 0;
  font-size: var(--font-size-md);
  color: var(--color-ink);
}

.card-remark {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  color: var(--color-ink-muted);
}

.card-totals {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-sm);
  margin: var(--space-sm) 0 0;
  padding-top: var(--space-sm);
  border-top: 1px solid var(--color-line);
}

.card-total {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.card-total span {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-cinnabar);
}

.paid-off {
  margin-left: var(--space-xs);
  font-size: var(--font-size-sm);
  font-style: normal;
  font-weight: 500;
  color: var(--color-pine);
}

.card-hint {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  color: var(--color-ink-muted);
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-xl) 0;
}

.empty-text {
  margin: 0;
  font-size: var(--font-size-md);
  color: var(--color-ink-muted);
}
</style>
