<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  cancelBooking,
  listBookings,
  markContacted,
  updateUnpaidAmount,
  type AdminBooking,
  type BookingStatus,
} from '../api/bookings'
import { ApiError } from '../api/http'
import { formatDateTime, formatRange } from '../lib/time'
import { currentStaff } from '../session'

const route = useRoute()
const router = useRouter()
const tableRef = ref<{ $el?: HTMLElement } | null>(null)
const loading = ref(false)
const acting = ref<string | null>(null)
const statusFilter = ref<BookingStatus | ''>('')
const rows = ref<AdminBooking[]>([])
const highlightId = ref('')
const followQuery = ref(true)

const statusLabel: Record<BookingStatus, string> = {
  pending: '待建联',
  contacted: '已建联',
  expired: '已取消',
}

const bookingQuery = computed(() => {
  const value = route.query.booking
  return typeof value === 'string' ? value : ''
})

const rowClassName = ({ row }: { row: AdminBooking }) =>
  row.id === highlightId.value ? 'is-booking-target' : ''

const load = async () => {
  const target = followQuery.value ? bookingQuery.value : ''
  highlightId.value = target
  const status = target ? '' : statusFilter.value
  if (target) statusFilter.value = ''
  loading.value = true
  try {
    rows.value = await listBookings(status)
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '加载失败')
  } finally {
    loading.value = false
  }
  if (!target) return
  await nextTick()
  tableRef.value?.$el
    ?.querySelector('.is-booking-target')
    ?.scrollIntoView({ block: 'center', behavior: 'smooth' })
}

const onStatusChange = () => {
  followQuery.value = false
  highlightId.value = ''
  if (bookingQuery.value) {
    void router.replace({ name: 'bookings', query: {} })
    return
  }
  void load()
}

const onContact = async (row: AdminBooking) => {
  try {
    await ElMessageBox.confirm(
      `确认已与 ${row.contact_name}（${row.contact_phone}）建联？`,
      '标为已建联',
      { type: 'warning' },
    )
  } catch {
    return
  }
  acting.value = row.id
  try {
    const updated = await markContacted(row.id)
    rows.value = rows.value.map((item) => (item.id === updated.id ? updated : item))
    ElMessage.success('已标记建联')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '操作失败')
  } finally {
    acting.value = null
  }
}

const formatMoney = (value: string | number) => `¥${Number(value).toFixed(2)}`

const onUnpaid = async (row: AdminBooking) => {
  let input: string
  try {
    const result = await ElMessageBox.prompt(
      `合计 ${formatMoney(row.total_price)}，请输入待付款（0～合计）`,
      '改待付款',
      {
        inputValue: row.unpaid_amount,
        inputPattern: /^(?:\d+)(?:\.\d{1,2})?$/,
        inputErrorMessage: '请输入最多两位小数的金额',
        confirmButtonText: '保存',
        cancelButtonText: '取消',
      },
    )
    input = String(result.value).trim()
  } catch {
    return
  }
  const amount = Number(input)
  if (Number.isNaN(amount) || amount < 0 || amount > Number(row.total_price)) {
    ElMessage.error('待付款须在 0 与合计之间')
    return
  }
  acting.value = row.id
  try {
    const updated = await updateUnpaidAmount(row.id, amount.toFixed(2))
    rows.value = rows.value.map((item) => (item.id === updated.id ? updated : item))
    ElMessage.success('已更新待付款')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '操作失败')
  } finally {
    acting.value = null
  }
}

const onCancel = async (row: AdminBooking) => {
  try {
    await ElMessageBox.confirm(
      `确认取消 ${row.contact_name} 的「${row.activity_name}」？名额将退回。`,
      '取消预约',
      { type: 'warning' },
    )
  } catch {
    return
  }
  acting.value = row.id
  try {
    const updated = await cancelBooking(row.id)
    rows.value = rows.value.map((item) => (item.id === updated.id ? updated : item))
    ElMessage.success('已取消预约')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '操作失败')
  } finally {
    acting.value = null
  }
}

watch(
  bookingQuery,
  () => {
    followQuery.value = true
    void load()
  },
  { immediate: true },
)
</script>

<template>
  <div>
    <div class="toolbar">
      <h2>{{ currentStaff?.camp_name ?? '预约' }}</h2>
      <el-select
        v-model="statusFilter"
        placeholder="全部状态"
        clearable
        style="width: 160px"
        @change="onStatusChange"
      >
        <el-option label="待建联" value="pending" />
        <el-option label="已建联" value="contacted" />
        <el-option label="已取消" value="expired" />
      </el-select>
    </div>
    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="rows"
      row-key="id"
      stripe
      :row-class-name="rowClassName"
    >
      <el-table-column label="活动" prop="activity_name" min-width="160" />
      <el-table-column label="预约场次" min-width="180">
        <template #default="{ row }">
          {{ formatRange(row.start_time, row.end_time) }}
        </template>
      </el-table-column>
      <el-table-column label="下单时间" min-width="140">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="联系人" min-width="90" prop="contact_name" />
      <el-table-column label="手机" min-width="120" prop="contact_phone" />
      <el-table-column label="人数" width="90">
        <template #default="{ row }"> {{ row.adult_count }} 大 {{ row.child_count }} 小 </template>
      </el-table-column>
      <el-table-column label="备注" min-width="100" prop="remark" show-overflow-tooltip />
      <el-table-column label="合计" width="100">
        <template #default="{ row }">{{ formatMoney(row.total_price) }}</template>
      </el-table-column>
      <el-table-column label="待付款" width="110">
        <template #default="{ row }">{{ formatMoney(row.unpaid_amount) }}</template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag
            :type="row.status === 'pending' ? 'warning' : row.status === 'contacted' ? 'success' : 'info'"
          >
            {{ statusLabel[row.status as BookingStatus] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="" width="220" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending'"
            type="primary"
            link
            :loading="acting === row.id"
            @click="onContact(row)"
          >
            已建联
          </el-button>
          <el-button
            v-if="row.status === 'pending' || row.status === 'contacted'"
            type="primary"
            link
            :loading="acting === row.id"
            @click="onUnpaid(row)"
          >
            改待付款
          </el-button>
          <el-button
            v-if="row.status === 'pending' || row.status === 'contacted'"
            type="danger"
            link
            :loading="acting === row.id"
            @click="onCancel(row)"
          >
            取消
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

h2 {
  margin: 0;
  font-size: 18px;
}

:deep(.is-booking-target td) {
  background: var(--el-color-primary-light-9) !important;
}
</style>
