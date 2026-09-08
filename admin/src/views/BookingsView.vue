<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  cancelBooking,
  listBookings,
  markContacted,
  type AdminBooking,
  type BookingStatus,
} from '../api/bookings'
import { ApiError } from '../api/http'
import { formatDateTime, formatRange } from '../lib/time'
import { currentStaff } from '../session'

const loading = ref(false)
const acting = ref<string | null>(null)
const statusFilter = ref<BookingStatus | ''>('')
const rows = ref<AdminBooking[]>([])

const statusLabel: Record<BookingStatus, string> = {
  pending: '待建联',
  contacted: '已建联',
  expired: '已取消',
}

const load = async () => {
  loading.value = true
  try {
    rows.value = await listBookings(statusFilter.value)
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '加载失败')
  } finally {
    loading.value = false
  }
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

onMounted(load)
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
        @change="load"
      >
        <el-option label="待建联" value="pending" />
        <el-option label="已建联" value="contacted" />
        <el-option label="已取消" value="expired" />
      </el-select>
    </div>
    <el-table v-loading="loading" :data="rows" stripe>
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
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag
            :type="row.status === 'pending' ? 'warning' : row.status === 'contacted' ? 'success' : 'info'"
          >
            {{ statusLabel[row.status as BookingStatus] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="" width="160" fixed="right">
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
</style>
