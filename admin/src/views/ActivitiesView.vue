<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  listAdminActivities,
  updateActivityPrices,
  updateSchedule,
  type AdminActivity,
} from '../api/catalog'
import { ApiError } from '../api/http'
import { formatRange } from '../lib/time'

const loading = ref(false)
const saving = ref<string | null>(null)
const activities = ref<AdminActivity[]>([])
const drafts = reactive<Record<string, { price: number; child_price: number }>>({})
const capacityDrafts = reactive<Record<string, number>>({})

const statusLabel: Record<string, string> = {
  pending: '待建联',
  contacted: '已建联',
}

const applyDrafts = (list: AdminActivity[]) => {
  activities.value = list
  for (const activity of list) {
    drafts[activity.id] = {
      price: Number(activity.price),
      child_price: Number(activity.child_price),
    }
    for (const schedule of activity.schedules) {
      capacityDrafts[schedule.id] = schedule.capacity
    }
  }
}

const replaceActivity = (updated: AdminActivity) => {
  activities.value = activities.value.map((item) => (item.id === updated.id ? updated : item))
  drafts[updated.id] = {
    price: Number(updated.price),
    child_price: Number(updated.child_price),
  }
  for (const schedule of updated.schedules) {
    capacityDrafts[schedule.id] = schedule.capacity
  }
}

const load = async () => {
  loading.value = true
  try {
    applyDrafts(await listAdminActivities())
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '加载失败')
  } finally {
    loading.value = false
  }
}

const onSavePrices = async (activity: AdminActivity) => {
  const draft = drafts[activity.id]
  if (!draft) return
  saving.value = activity.id
  try {
    replaceActivity(
      await updateActivityPrices(activity.id, String(draft.price), String(draft.child_price)),
    )
    ElMessage.success('价格已保存，已有预约金额不变')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '保存失败')
  } finally {
    saving.value = null
  }
}

const onSaveCapacity = async (scheduleId: string) => {
  const capacity = capacityDrafts[scheduleId]
  saving.value = scheduleId
  try {
    replaceActivity(await updateSchedule(scheduleId, { capacity }))
    ElMessage.success('名额已更新')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '名额不能小于已订人数')
  } finally {
    saving.value = null
  }
}

const onToggleSchedule = async (scheduleId: string, next: 'open' | 'closed') => {
  const label = next === 'closed' ? '关闭该场次？游客将无法再预约，已有预约保留。' : '重新开放该场次？'
  try {
    await ElMessageBox.confirm(label, next === 'closed' ? '关闭场次' : '开放场次', {
      type: 'warning',
    })
  } catch {
    return
  }
  saving.value = scheduleId
  try {
    replaceActivity(await updateSchedule(scheduleId, { status: next }))
    ElMessage.success(next === 'closed' ? '场次已关闭' : '场次已开放')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '操作失败')
  } finally {
    saving.value = null
  }
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <h2>活动排期</h2>
    <p class="hint">改价不影响已下单金额。关场次不删除已有预约。</p>
    <el-card v-for="activity in activities" :key="activity.id" class="card" shadow="never">
      <div class="activity-head">
        <h3>{{ activity.name }}</h3>
        <div class="prices">
          <span>成人</span>
          <el-input-number
            v-if="drafts[activity.id]"
            v-model="drafts[activity.id].price"
            :min="0"
            :precision="2"
            :step="1"
            controls-position="right"
          />
          <span>儿童</span>
          <el-input-number
            v-if="drafts[activity.id]"
            v-model="drafts[activity.id].child_price"
            :min="0"
            :precision="2"
            :step="1"
            controls-position="right"
          />
          <el-button
            type="primary"
            :loading="saving === activity.id"
            @click="onSavePrices(activity)"
          >
            保存价格
          </el-button>
        </div>
      </div>
      <el-table :data="activity.schedules" row-key="id">
        <el-table-column type="expand">
          <template #default="{ row }">
            <el-table v-if="row.bookings.length" :data="row.bookings" size="small">
              <el-table-column label="预约场次" min-width="180">
                <template #default="{ row: booking }">
                  {{ formatRange(booking.start_time, booking.end_time) }}
                </template>
              </el-table-column>
              <el-table-column label="联系人" prop="contact_name" width="100" />
              <el-table-column label="手机" prop="contact_phone" width="130" />
              <el-table-column label="人数" width="100">
                <template #default="{ row: booking }">
                  {{ booking.adult_count }} 大 {{ booking.child_count }} 小
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="{ row: booking }">
                  {{ statusLabel[booking.status] ?? booking.status }}
                </template>
              </el-table-column>
            </el-table>
            <p v-else class="empty">该场暂无有效预约</p>
          </template>
        </el-table-column>
        <el-table-column label="场次时间" min-width="200">
          <template #default="{ row }">
            {{ formatRange(row.start_time, row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="已订 / 名额" min-width="220">
          <template #default="{ row }">
            <span>{{ row.booked_count }} / </span>
            <el-input-number
              v-model="capacityDrafts[row.id]"
              :min="row.booked_count"
              :step="1"
              controls-position="right"
              size="small"
            />
            <el-button
              link
              type="primary"
              :loading="saving === row.id"
              @click="onSaveCapacity(row.id)"
            >
              保存
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="余位" width="80" prop="remaining" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'open' ? 'success' : 'info'">
              {{ row.status === 'open' ? '开放' : '已关闭' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="" width="100">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'open'"
              link
              type="danger"
              :loading="saving === row.id"
              @click="onToggleSchedule(row.id, 'closed')"
            >
              关闭
            </el-button>
            <el-button
              v-else
              link
              type="primary"
              :loading="saving === row.id"
              @click="onToggleSchedule(row.id, 'open')"
            >
              开放
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
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

.card {
  margin-bottom: 16px;
}

.activity-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

h3 {
  margin: 0;
  font-size: 16px;
}

.prices {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.empty {
  margin: 0;
  padding: 8px 16px;
  color: var(--el-text-color-secondary);
}
</style>
