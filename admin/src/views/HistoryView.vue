<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listHistory, type HistoryBooking, type HistorySchedule } from '../api/history'
import { ApiError } from '../api/http'
import { formatRange, shanghaiDateKey } from '../lib/time'

const router = useRouter()
const loading = ref(false)
const schedules = ref<HistorySchedule[]>([])
const dateRange = ref<[string, string] | null>(null)
const activityId = ref('')
const contactName = ref('')
const contactPhone = ref('')

const statusLabel: Record<string, string> = {
  pending: '待建联',
  contacted: '已建联',
  expired: '已取消',
}

type HistoryRow = {
  key: string
  schedule: HistorySchedule
  booking: HistoryBooking | null
}

const formatMoney = (value: string | number) => `¥${Number(value).toFixed(2)}`

const activityOptions = computed(() => {
  const names = new Map<string, string>()
  for (const schedule of schedules.value) {
    names.set(schedule.activity_id, schedule.activity_name)
  }
  return [...names.entries()].map(([id, name]) => ({ id, name }))
})

const rows = computed((): HistoryRow[] => {
  const name = contactName.value.trim()
  const phone = contactPhone.value.trim()
  const searchingCustomer = Boolean(name || phone)
  const [from, to] = dateRange.value ?? []
  const matched: HistoryRow[] = []

  for (const schedule of schedules.value) {
    if (activityId.value && schedule.activity_id !== activityId.value) continue
    const day = shanghaiDateKey(schedule.start_time)
    if (from && day < from) continue
    if (to && day > to) continue

    const bookings = searchingCustomer
      ? schedule.bookings.filter((booking) => {
          const nameOk = !name || booking.contact_name.includes(name)
          const phoneOk = !phone || booking.contact_phone.includes(phone)
          return nameOk && phoneOk
        })
      : schedule.bookings

    if (searchingCustomer && bookings.length === 0) continue
    if (bookings.length === 0) {
      matched.push({ key: schedule.id, schedule, booking: null })
      continue
    }
    for (const booking of bookings) {
      matched.push({ key: `${schedule.id}-${booking.id}`, schedule, booking })
    }
  }
  return matched
})

const load = async () => {
  loading.value = true
  try {
    schedules.value = await listHistory()
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '加载失败')
  } finally {
    loading.value = false
  }
}

const openBooking = (bookingId: string) => {
  void router.push({ name: 'bookings', query: { booking: bookingId } })
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <h2>历史活动</h2>
    <p class="hint">查看开始日早于今天的场次，以及这些场次的预约客户。已取消的预约也会出现。</p>

    <div class="filters">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        value-format="YYYY-MM-DD"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        clearable
      />
      <el-select v-model="activityId" placeholder="全部活动" clearable filterable style="width: 220px">
        <el-option
          v-for="activity in activityOptions"
          :key="activity.id"
          :label="activity.name"
          :value="activity.id"
        />
      </el-select>
      <el-input v-model="contactName" placeholder="客户姓名" clearable style="width: 160px" />
      <el-input v-model="contactPhone" placeholder="电话号码" clearable style="width: 180px" />
    </div>

    <el-table v-if="rows.length" :data="rows" row-key="key" stripe>
      <el-table-column label="活动" min-width="160">
        <template #default="{ row }">
          {{ row.schedule.activity_name }}
        </template>
      </el-table-column>
      <el-table-column label="场次时间" min-width="180">
        <template #default="{ row }">
          {{ formatRange(row.schedule.start_time, row.schedule.end_time) }}
        </template>
      </el-table-column>
      <el-table-column label="联系人" min-width="120">
        <template #default="{ row }">
          <el-button v-if="row.booking" type="primary" link @click="openBooking(row.booking.id)">
            {{ row.booking.contact_name }}
          </el-button>
          <span v-else class="muted">暂无预约</span>
        </template>
      </el-table-column>
      <el-table-column label="手机" min-width="130">
        <template #default="{ row }">
          {{ row.booking?.contact_phone ?? '—' }}
        </template>
      </el-table-column>
      <el-table-column label="人数" width="110">
        <template #default="{ row }">
          <template v-if="row.booking">
            {{ row.booking.adult_count }} 大 {{ row.booking.child_count }} 小
          </template>
          <span v-else>—</span>
        </template>
      </el-table-column>
      <el-table-column label="合计" width="110">
        <template #default="{ row }">
          {{ row.booking ? formatMoney(row.booking.total_price) : '—' }}
        </template>
      </el-table-column>
      <el-table-column label="待付款" width="110">
        <template #default="{ row }">
          {{ row.booking ? formatMoney(row.booking.unpaid_amount) : '—' }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <template v-if="row.booking">
            {{ statusLabel[row.booking.status] ?? row.booking.status }}
          </template>
          <span v-else>—</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" min-width="140" show-overflow-tooltip>
        <template #default="{ row }">
          {{ row.booking?.remark || '—' }}
        </template>
      </el-table-column>
    </el-table>
    <p v-else-if="!loading" class="empty">没有符合条件的历史排期</p>
  </div>
</template>

<style scoped>
h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

.hint {
  margin: 0 0 16px;
  color: var(--el-text-color-secondary);
}

.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.empty,
.muted {
  color: var(--el-text-color-secondary);
}

.empty {
  margin: 0;
}
</style>
