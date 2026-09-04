<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import {
  getBookingById,
  updateBookingStatus,
  type BookingStatus,
} from '../data/bookings'

const route = useRoute()
const router = useRouter()

const booking = computed(() => getBookingById(String(route.params.id)))

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

const formatTime = (ts: number) => {
  if (!ts) return '—'
  const d = new Date(ts)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void router.push({ name: 'bookings' })
}

const onCancel = () => {
  const item = booking.value
  if (!item) return
  showConfirmDialog({
    className: 'ab-dialog',
    title: '取消预约',
    message: '确定取消这次预约吗？取消后状态会变为失效。',
    confirmButtonText: '确认取消',
    cancelButtonText: '再想想',
  })
    .then(() => {
      updateBookingStatus(item.id, 'expired')
      showToast('已取消')
      void router.replace({ name: 'bookings' })
    })
    .catch(() => {})
}
</script>

<template>
  <div class="ab-page">
    <van-nav-bar
      title="预约详情"
      left-arrow
      safe-area-inset-top
      @click-left="goBack"
    />

    <div v-if="!booking" class="page-body">
      <p class="missing">预约不存在</p>
    </div>

    <div v-else class="page-body">
      <section class="card">
        <div class="head">
          <h1 class="ab-title title">{{ booking.title }}</h1>
          <van-tag :type="statusType[booking.status]">
            {{ statusLabel[booking.status] }}
          </van-tag>
        </div>
        <p class="session">{{ booking.sessionLabel }}</p>
        <dl class="rows">
          <div class="row">
            <dt>姓名</dt>
            <dd>{{ booking.name }}</dd>
          </div>
          <div class="row">
            <dt>人数</dt>
            <dd>
              成人 {{ booking.count }}
              <template v-if="booking.childCount">
                · 儿童 {{ booking.childCount }}
              </template>
            </dd>
          </div>
          <div class="row">
            <dt>手机号</dt>
            <dd>{{ booking.phone }}</dd>
          </div>
          <div v-if="booking.remark" class="row">
            <dt>备注</dt>
            <dd>{{ booking.remark }}</dd>
          </div>
          <div class="row">
            <dt>提交时间</dt>
            <dd>{{ formatTime(booking.createdAt) }}</dd>
          </div>
        </dl>
        <p class="total">合计 <span>¥{{ booking.totalPrice }}</span></p>
      </section>

      <van-button
        v-if="booking.status === 'pending'"
        class="cancel"
        block
        @click="onCancel"
      >
        取消预约
      </van-button>
    </div>
  </div>
</template>

<style scoped>
.page-body {
  padding: var(--space-md);
}

.missing {
  margin: var(--space-xl) 0 0;
  color: var(--color-ink-muted);
}

.card {
  padding: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-sm);
}

.title {
  font-size: var(--font-size-xl);
}

.session {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-pine);
}

.rows {
  margin: var(--space-md) 0 0;
  padding: 0;
}

.row {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-sm) 0;
  border-top: 1px solid var(--color-line);
}

.row dt {
  flex: 0 0 64px;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.row dd {
  flex: 1;
  margin: 0;
  font-size: var(--font-size-md);
  color: var(--color-ink);
}

.total {
  margin: 0;
  padding-top: var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
  border-top: 1px solid var(--color-line);
}

.total span {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-cinnabar);
}

.cancel {
  margin-top: var(--space-lg);
  color: var(--color-cinnabar);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
}
</style>
