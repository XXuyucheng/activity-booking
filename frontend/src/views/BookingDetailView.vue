<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import {
  cancelBooking,
  fetchBooking,
  type BookingResponse,
} from '../api/bookings'
import { ApiError, redirectToLogin } from '../api/http'
import { clearOAuthReturn } from '../lib/oauthReturn'
import { formatClockRange, formatDateTime } from '../lib/schedules'
import { useCampRouter } from '../lib/campRoute'
import { PAYMENT_HINT, isPaidOff } from '../data/booking-copy'

const route = useRoute()
const { campSlug, push, replace, router } = useCampRouter()
const booking = ref<BookingResponse | null>(null)
const missing = ref(false)
const cancelling = ref(false)

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
  missing.value = false
  try {
    const detail = await fetchBooking(String(route.params.id))
    if (detail.camp_slug !== campSlug.value) {
      booking.value = null
      missing.value = true
      return
    }
    booking.value = detail
  } catch (error) {
    booking.value = null
    if (error instanceof ApiError && error.status === 401) {
      clearOAuthReturn()
      redirectToLogin()
      return
    }
    missing.value = true
  }
}

watch(
  () => [route.params.id, campSlug.value],
  () => {
    void load()
  },
  { immediate: true },
)

const goBack = () => {
  if (window.history.state?.back) {
    router.back()
    return
  }
  void push('bookings')
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
    .then(async () => {
      cancelling.value = true
      try {
        await cancelBooking(item.id)
        showToast('已取消')
        void replace('bookings')
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          clearOAuthReturn()
          redirectToLogin()
          return
        }
        const message =
          error instanceof ApiError && error.message === 'too late to cancel'
            ? '开始前 24 小时内不可取消'
            : error instanceof Error
              ? error.message
              : '取消失败'
        showToast(message)
      } finally {
        cancelling.value = false
      }
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

    <div v-if="missing" class="page-body">
      <p class="missing">预约不存在</p>
    </div>

    <div v-else-if="booking" class="page-body">
      <section class="card">
        <div class="head">
          <h1 class="ab-title title">{{ booking.activity_name }}</h1>
          <van-tag :type="statusType[booking.status] ?? 'default'">
            {{ statusLabel[booking.status] ?? booking.status }}
          </van-tag>
        </div>
        <p class="session">
          {{ formatClockRange(booking.start_time, booking.end_time) }}
        </p>
        <dl class="rows">
          <div class="row">
            <dt>姓名</dt>
            <dd>{{ booking.contact_name }}</dd>
          </div>
          <div class="row">
            <dt>人数</dt>
            <dd>
              成人 {{ booking.adult_count }}
              <template v-if="booking.child_count">
                · 儿童 {{ booking.child_count }}
              </template>
            </dd>
          </div>
          <div class="row">
            <dt>手机号</dt>
            <dd>{{ booking.contact_phone }}</dd>
          </div>
          <div v-if="booking.remark" class="row">
            <dt>备注</dt>
            <dd>{{ booking.remark }}</dd>
          </div>
          <div class="row">
            <dt>提交时间</dt>
            <dd>{{ formatDateTime(booking.created_at) }}</dd>
          </div>
        </dl>
        <div class="totals">
          <p class="total">合计 <span>¥{{ booking.total_price }}</span></p>
          <p class="total">
            待付款 <span>¥{{ booking.unpaid_amount }}</span>
            <em v-if="isPaidOff(booking.unpaid_amount)" class="paid-off">已付清</em>
          </p>
        </div>
        <p class="pay-hint">{{ PAYMENT_HINT }}</p>
      </section>

      <van-button
        v-if="booking.status === 'pending'"
        class="cancel"
        block
        :loading="cancelling"
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

.totals {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-sm);
  margin: 0;
  padding-top: var(--space-sm);
  border-top: 1px solid var(--color-line);
}

.total {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.total span {
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

.pay-hint {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  color: var(--color-ink-muted);
}

.cancel {
  margin-top: var(--space-lg);
  color: var(--color-cinnabar);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
}
</style>
