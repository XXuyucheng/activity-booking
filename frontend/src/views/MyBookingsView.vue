<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  loadBookings,
  type BookingRecord,
  type BookingStatus,
} from '../data/bookings'
import { getActivityById } from '../data/mock-activities'

const router = useRouter()
const list = ref<BookingRecord[]>([])

const statusLabel: Record<BookingStatus, string> = {
  pending: '已预约待建联',
  contacted: '已建联',
  expired: '失效',
}

const statusType: Record<BookingStatus, 'primary' | 'success' | 'default'> = {
  pending: 'primary',
  contacted: 'success',
  expired: 'default',
}

onMounted(() => {
  list.value = loadBookings()
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

const openDetail = (id: string) => {
  void router.push({ name: 'booking-detail', params: { id } })
}

const coverOf = (item: BookingRecord) =>
  getActivityById(item.activityId)?.cover
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
      <template v-if="list.length">
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
                <h2 class="ab-title card-title">{{ item.title }}</h2>
                <van-tag :type="statusType[item.status]">
                  {{ statusLabel[item.status] }}
                </van-tag>
                <span class="card-arrow">›</span>
              </div>
              <p class="card-session">{{ item.sessionLabel }}</p>
              <p class="card-meta">
                {{ item.name }} · 成人 {{ item.count }}
                <template v-if="item.childCount">· 儿童 {{ item.childCount }}</template>
                · {{ item.phone }}
              </p>
              <p v-if="item.remark" class="card-remark">备注：{{ item.remark }}</p>
              <p class="card-total">合计 <span>¥{{ item.totalPrice }}</span></p>
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

.card-total {
  margin: var(--space-sm) 0 0;
  padding-top: var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
  border-top: 1px solid var(--color-line);
}

.card-total span {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-cinnabar);
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
