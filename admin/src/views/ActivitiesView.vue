<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  createSchedule,
  listAdminActivities,
  updateActivityPrices,
  updateSchedule,
  type AdminActivity,
  type AdminSchedule,
} from '../api/catalog'
import { ApiError } from '../api/http'
import { formatRange } from '../lib/time'

const router = useRouter()
const loading = ref(false)
const saving = ref<string | null>(null)
const activities = ref<AdminActivity[]>([])
const selectedActivityId = ref('')
const selectedScheduleId = ref('')
const expandedActivityIds = ref<string[]>([])
const drafts = reactive<Record<string, { price: number; child_price: number }>>({})
const capacityDrafts = reactive<Record<string, number>>({})
const creating = ref(false)
const createActivityId = ref('')
const createStart = ref<Date | null>(null)
const createEnd = ref<Date | null>(null)
const createCapacity = ref(10)
const createPrice = ref(0)
const createChildPrice = ref(0)

const statusLabel: Record<string, string> = {
  pending: '待建联',
  contacted: '已建联',
}

const formatMoney = (value: string | number) => `¥${Number(value).toFixed(2)}`

const selectedActivity = computed(
  () => activities.value.find((item) => item.id === selectedActivityId.value) ?? null,
)

const selectedSchedule = computed((): AdminSchedule | null => {
  const activity = selectedActivity.value
  if (!activity) return null
  return activity.schedules.find((item) => item.id === selectedScheduleId.value) ?? null
})

const keepSelection = (activityId: string, scheduleId: string) => {
  const activity = activities.value.find((item) => item.id === activityId)
  if (activity) {
    selectedActivityId.value = activity.id
    const schedule =
      activity.schedules.find((item) => item.id === scheduleId) ?? activity.schedules[0]
    selectedScheduleId.value = schedule?.id ?? ''
    return
  }
  const first = activities.value[0]
  selectedActivityId.value = first?.id ?? ''
  selectedScheduleId.value = first?.schedules[0]?.id ?? ''
}

const ensureExpanded = (activityId: string) => {
  if (!activityId || expandedActivityIds.value.includes(activityId)) return
  expandedActivityIds.value = [...expandedActivityIds.value, activityId]
}

const isActivityOpen = (activityId: string) => expandedActivityIds.value.includes(activityId)

const toggleActivity = (activityId: string) => {
  expandedActivityIds.value = isActivityOpen(activityId)
    ? expandedActivityIds.value.filter((id) => id !== activityId)
    : [...expandedActivityIds.value, activityId]
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

const fillCreatePrices = (activityId: string) => {
  const draft = drafts[activityId]
  if (draft) {
    createPrice.value = draft.price
    createChildPrice.value = draft.child_price
    return
  }
  const activity = activities.value.find((item) => item.id === activityId)
  if (!activity) return
  createPrice.value = Number(activity.price)
  createChildPrice.value = Number(activity.child_price)
}

const replaceActivity = (updated: AdminActivity, scheduleId?: string) => {
  activities.value = activities.value.map((item) => (item.id === updated.id ? updated : item))
  drafts[updated.id] = {
    price: Number(updated.price),
    child_price: Number(updated.child_price),
  }
  for (const schedule of updated.schedules) {
    capacityDrafts[schedule.id] = schedule.capacity
  }
  keepSelection(
    scheduleId ? updated.id : selectedActivityId.value,
    scheduleId ?? selectedScheduleId.value,
  )
}

const load = async () => {
  loading.value = true
  try {
    applyDrafts(await listAdminActivities())
    keepSelection(selectedActivityId.value, selectedScheduleId.value)
    ensureExpanded(selectedActivityId.value)
    if (!createActivityId.value) {
      createActivityId.value = selectedActivityId.value
      fillCreatePrices(createActivityId.value)
    }
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '加载失败')
  } finally {
    loading.value = false
  }
}

watch(selectedActivityId, (activityId, previous) => {
  if (activityId && activityId !== previous) ensureExpanded(activityId)
  if (!previous || activityId === previous) return
  const activity = activities.value.find((item) => item.id === activityId)
  selectedScheduleId.value = activity?.schedules[0]?.id ?? ''
})

watch(createActivityId, (activityId) => {
  if (activityId) fillCreatePrices(activityId)
})

const onCreateSchedule = async () => {
  if (!createActivityId.value || !createStart.value || !createEnd.value) {
    ElMessage.error('请填写活动、开始和结束时间')
    return
  }
  if (createEnd.value <= createStart.value) {
    ElMessage.error('结束时间须晚于开始时间')
    return
  }
  if (createCapacity.value < 1) {
    ElMessage.error('总位数至少为 1')
    return
  }
  const prev = new Set(
    (activities.value.find((item) => item.id === createActivityId.value)?.schedules ?? []).map(
      (item) => item.id,
    ),
  )
  creating.value = true
  try {
    const updated = await createSchedule(createActivityId.value, {
      start_time: createStart.value.toISOString(),
      end_time: createEnd.value.toISOString(),
      capacity: createCapacity.value,
      price: createPrice.value.toFixed(2),
      child_price: createChildPrice.value.toFixed(2),
    })
    const created = updated.schedules.find((item) => !prev.has(item.id))
    replaceActivity(updated, created?.id)
    ensureExpanded(updated.id)
    fillCreatePrices(updated.id)
    createStart.value = null
    createEnd.value = null
    ElMessage.success('排期已创建')
  } catch (error) {
    ElMessage.error(error instanceof ApiError ? error.message : '创建失败')
  } finally {
    creating.value = false
  }
}

const onSavePrices = async () => {
  const activity = selectedActivity.value
  const draft = activity ? drafts[activity.id] : undefined
  if (!activity || !draft) return
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

const openBooking = (bookingId: string) => {
  void router.push({ name: 'bookings', query: { booking: bookingId } })
}

const selectSlot = (activityId: string, scheduleId: string) => {
  selectedActivityId.value = activityId
  selectedScheduleId.value = scheduleId
}

const onScheduleRowClick = (activityId: string, row: AdminSchedule) => {
  selectSlot(activityId, row.id)
}

const scheduleRowClass = ({ row }: { row: AdminSchedule }) =>
  row.id === selectedScheduleId.value ? 'is-slot-current' : ''

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <h2>活动排期</h2>
    <p class="hint">
      上方创建新场次。改价不影响已下单金额。关场次不删除已有预约。点联系人可跳到预约建联。
    </p>

    <el-card class="create-card" shadow="never">
      <h3>创建排期</h3>
      <p class="card-desc">
        给已有活动加一场。价格是该活动现价，改了会影响该活动所有未下单展示价；已下单金额不变。新场次默认开放。
      </p>
      <div class="create-form">
        <el-select
          v-model="createActivityId"
          placeholder="选择活动"
          filterable
          style="width: 220px"
        >
          <el-option
            v-for="activity in activities"
            :key="activity.id"
            :label="activity.name"
            :value="activity.id"
          />
        </el-select>
        <el-date-picker
          v-model="createStart"
          type="datetime"
          placeholder="开始时间"
          style="width: 200px"
        />
        <el-date-picker
          v-model="createEnd"
          type="datetime"
          placeholder="结束时间"
          style="width: 200px"
        />
        <span>总位数</span>
        <el-input-number
          v-model="createCapacity"
          :min="1"
          :step="1"
          controls-position="right"
        />
        <span>成人价</span>
        <el-input-number
          v-model="createPrice"
          :min="0"
          :precision="2"
          :step="1"
          controls-position="right"
        />
        <span>儿童价</span>
        <el-input-number
          v-model="createChildPrice"
          :min="0"
          :precision="2"
          :step="1"
          controls-position="right"
        />
        <el-button type="primary" :loading="creating" @click="onCreateSchedule">
          创建排期
        </el-button>
      </div>
    </el-card>

    <el-card class="filter-card" shadow="never">
      <h3>排期筛选</h3>
      <p class="card-desc">选择已有活动和场次，查看该场预约、改名额或开关场次。</p>
      <div class="filters">
        <el-select v-model="selectedActivityId" placeholder="选择活动" filterable style="width: 280px">
          <el-option
            v-for="activity in activities"
            :key="activity.id"
            :label="activity.name"
            :value="activity.id"
          />
        </el-select>
        <el-select v-model="selectedScheduleId" placeholder="选择场次" filterable style="width: 280px">
          <el-option
            v-for="schedule in selectedActivity?.schedules ?? []"
            :key="schedule.id"
            :label="formatRange(schedule.start_time, schedule.end_time)"
            :value="schedule.id"
          />
        </el-select>
      </div>

      <template v-if="selectedActivity && selectedSchedule">
      <div class="activity-head">
        <h3>{{ selectedActivity.name }}</h3>
        <div class="prices">
          <span>当前成人价</span>
          <el-input-number
            v-if="drafts[selectedActivity.id]"
            v-model="drafts[selectedActivity.id].price"
            :min="0"
            :precision="2"
            :step="1"
            controls-position="right"
          />
          <span>当前儿童价</span>
          <el-input-number
            v-if="drafts[selectedActivity.id]"
            v-model="drafts[selectedActivity.id].child_price"
            :min="0"
            :precision="2"
            :step="1"
            controls-position="right"
          />
          <el-button
            type="primary"
            :loading="saving === selectedActivity.id"
            @click="onSavePrices"
          >
            保存价格
          </el-button>
        </div>
      </div>

      <div class="slot-meta">
        <span>场次 {{ formatRange(selectedSchedule.start_time, selectedSchedule.end_time) }}</span>
        <el-tag :type="selectedSchedule.status === 'open' ? 'success' : 'info'">
          {{ selectedSchedule.status === 'open' ? '开放' : '已关闭' }}
        </el-tag>
        <strong>该场实收 {{ formatMoney(selectedSchedule.revenue) }}</strong>
        <span>已订 {{ selectedSchedule.booked_count }} / 余位 {{ selectedSchedule.remaining }}</span>
        <el-input-number
          v-model="capacityDrafts[selectedSchedule.id]"
          :min="selectedSchedule.booked_count"
          :step="1"
          controls-position="right"
          size="small"
        />
        <el-button
          link
          type="primary"
          :loading="saving === selectedSchedule.id"
          @click="onSaveCapacity(selectedSchedule.id)"
        >
          保存名额
        </el-button>
        <el-button
          v-if="selectedSchedule.status === 'open'"
          link
          type="danger"
          :loading="saving === selectedSchedule.id"
          @click="onToggleSchedule(selectedSchedule.id, 'closed')"
        >
          关闭场次
        </el-button>
        <el-button
          v-else
          link
          type="primary"
          :loading="saving === selectedSchedule.id"
          @click="onToggleSchedule(selectedSchedule.id, 'open')"
        >
          开放场次
        </el-button>
      </div>

      <el-table v-if="selectedSchedule.bookings.length" :data="selectedSchedule.bookings" stripe>
        <el-table-column label="预约场次" min-width="180">
          <template #default="{ row }">
            {{ formatRange(row.start_time, row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="联系人" min-width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="openBooking(row.id)">
              {{ row.contact_name }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="手机" prop="contact_phone" min-width="120" />
        <el-table-column label="人数" width="110">
          <template #default="{ row }"> {{ row.adult_count }} 大 {{ row.child_count }} 小 </template>
        </el-table-column>
        <el-table-column label="该单金额" width="110">
          <template #default="{ row }">
            {{ formatMoney(row.total_price) }}
          </template>
        </el-table-column>
        <el-table-column label="待付款" width="110">
          <template #default="{ row }">
            {{ formatMoney(row.unpaid_amount) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            {{ statusLabel[row.status] ?? row.status }}
          </template>
        </el-table-column>
      </el-table>
      <p v-else class="empty">该场暂无有效预约</p>
      </template>
      <p v-else-if="!loading" class="empty">请选择活动和场次</p>
    </el-card>

    <section v-for="activity in activities" :key="activity.id" class="all-slots">
      <button
        type="button"
        class="all-slots-toggle"
        :aria-expanded="isActivityOpen(activity.id)"
        @click="toggleActivity(activity.id)"
      >
        <span class="all-slots-title">{{ activity.name }}</span>
        <span class="all-slots-count">{{ activity.schedules.length }} 场</span>
        <span class="all-slots-arrow" :class="{ 'is-open': isActivityOpen(activity.id) }" />
      </button>
      <el-table
        v-if="isActivityOpen(activity.id)"
        :data="activity.schedules"
        row-key="id"
        :row-class-name="scheduleRowClass"
        @row-click="onScheduleRowClick.bind(null, activity.id)"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <el-table v-if="row.bookings.length" :data="row.bookings" size="small">
              <el-table-column label="预约场次" min-width="180">
                <template #default="{ row: booking }">
                  {{ formatRange(booking.start_time, booking.end_time) }}
                </template>
              </el-table-column>
              <el-table-column label="联系人" min-width="100">
                <template #default="{ row: booking }">
                  <el-button type="primary" link @click.stop="openBooking(booking.id)">
                    {{ booking.contact_name }}
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column label="手机" prop="contact_phone" width="130" />
              <el-table-column label="人数" width="100">
                <template #default="{ row: booking }">
                  {{ booking.adult_count }} 大 {{ booking.child_count }} 小
                </template>
              </el-table-column>
              <el-table-column label="该单金额" width="110">
                <template #default="{ row: booking }">
                  {{ formatMoney(booking.total_price) }}
                </template>
              </el-table-column>
              <el-table-column label="待付款" width="110">
                <template #default="{ row: booking }">
                  {{ formatMoney(booking.unpaid_amount) }}
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="{ row: booking }">
                  {{ statusLabel[booking.status] ?? booking.status }}
                </template>
              </el-table-column>
            </el-table>
            <p v-else class="empty nested">该场暂无有效预约</p>
          </template>
        </el-table-column>
        <el-table-column label="场次时间" min-width="200">
          <template #default="{ row }">
            {{ formatRange(row.start_time, row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="该场实收" width="120">
          <template #default="{ row }">
            {{ formatMoney(row.revenue) }}
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
              @click.stop
            />
            <el-button
              link
              type="primary"
              :loading="saving === row.id"
              @click.stop="onSaveCapacity(row.id)"
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
        <el-table-column label="" width="80">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'open'"
              link
              type="danger"
              :loading="saving === row.id"
              @click.stop="onToggleSchedule(row.id, 'closed')"
            >
              关闭
            </el-button>
            <el-button
              v-else
              link
              type="primary"
              :loading="saving === row.id"
              @click.stop="onToggleSchedule(row.id, 'open')"
            >
              开放
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>
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

.create-card,
.filter-card {
  margin-bottom: 16px;
}

.card-desc {
  margin: 0 0 12px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.create-form,
.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.filters {
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

.prices,
.slot-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.slot-meta {
  margin-bottom: 16px;
}

.empty {
  margin: 0;
  color: var(--el-text-color-secondary);
}

.empty.nested {
  padding: 8px 16px;
}

.all-slots {
  margin-top: 16px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.all-slots-toggle {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font: inherit;
}

.all-slots-title {
  margin-right: 8px;
  font-size: 16px;
  font-weight: 600;
}

.all-slots-count {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.all-slots-arrow {
  margin-left: auto;
  width: 8px;
  height: 8px;
  border-right: 2px solid var(--el-text-color-secondary);
  border-bottom: 2px solid var(--el-text-color-secondary);
  transform: rotate(45deg);
  transition: transform 0.2s;
}

.all-slots-arrow.is-open {
  transform: rotate(225deg);
}

:deep(.is-slot-current td) {
  background: var(--el-color-primary-light-9) !important;
}
</style>
