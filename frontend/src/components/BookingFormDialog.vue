<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

export type BookingPayload = {
  name: string
  count: number
  childCount: number
  phone: string
  remark: string
}

const props = defineProps<{
  show: boolean
  sessionLabel: string
  maxCount: number
  price: number
  childPrice: number
  notice: string
  activityId: string
  submitting?: boolean
}>()

const router = useRouter()

const emit = defineEmits<{
  'update:show': [value: boolean]
  submit: [payload: BookingPayload]
}>()

const name = ref('')
const count = ref(1)
const childCount = ref(0)
const phone = ref('')
const remark = ref('')

const phonePattern = /^1[3-9]\d{9}$/

const phoneRules = [
  { required: true, message: '请输入手机号' },
  {
    validator: (value: string) => phonePattern.test(value),
    message: '请输入正确的手机号',
  },
]

const remaining = computed(() => Math.max(props.maxCount, 0))
const adultMax = computed(() =>
  Math.max(remaining.value - childCount.value, 1),
)
const childMax = computed(() =>
  Math.max(remaining.value - count.value, 0),
)

const reset = () => {
  name.value = ''
  count.value = 1
  childCount.value = 0
  phone.value = ''
  remark.value = ''
}

watch(
  () => props.show,
  (value) => {
    if (value) reset()
  },
)

watch([count, childCount, remaining], () => {
  if (count.value > adultMax.value) count.value = adultMax.value
  if (childCount.value > childMax.value) childCount.value = childMax.value
  if (count.value < 1) count.value = 1
})

const total = computed(
  () => props.price * count.value + props.childPrice * childCount.value,
)

const close = () => {
  if (props.submitting) return
  emit('update:show', false)
}

const openRules = () => {
  close()
  void router.push({ name: 'rules', query: { activityId: props.activityId } })
}

const onSubmit = () => {
  if (props.submitting) return
  if (count.value + childCount.value > remaining.value) return
  emit('submit', {
    name: name.value.trim(),
    count: count.value,
    childCount: childCount.value,
    phone: phone.value.trim(),
    remark: remark.value.trim(),
  })
}
</script>

<template>
  <van-popup
    :show="show"
    position="center"
    round
    class="dialog"
    :close-on-click-overlay="!submitting"
    @update:show="emit('update:show', $event)"
  >
    <div class="head">
      <div class="head-copy">
        <h2 class="ab-title head-title">预约活动</h2>
        <p class="head-session">{{ sessionLabel }}</p>
      </div>
      <button type="button" class="head-close" aria-label="关闭" @click="close">
        ×
      </button>
    </div>

    <van-form class="form" @submit="onSubmit">
      <div class="notice">
        <p class="notice-text">{{ notice }}</p>
        <button type="button" class="notice-link" @click="openRules">
          查看详情
        </button>
      </div>
      <van-cell-group inset class="group">
        <van-field
          v-model="name"
          name="name"
          label="姓名"
          placeholder="请输入姓名"
          required
          :rules="[{ required: true, message: '请输入姓名' }]"
        />
        <van-field name="count" label="成人">
          <template #input>
            <van-stepper v-model="count" integer min="1" :max="adultMax" />
          </template>
        </van-field>
        <van-field name="childCount" label="儿童">
          <template #input>
            <van-stepper v-model="childCount" integer min="0" :max="childMax" />
          </template>
        </van-field>
        <van-field
          v-model="phone"
          name="phone"
          type="tel"
          maxlength="11"
          label="手机号"
          placeholder="用于接收预约通知"
          required
          :rules="phoneRules"
        />
        <van-field
          v-model="remark"
          name="remark"
          type="textarea"
          rows="2"
          autosize
          label="备注"
          placeholder="其他需求、儿童年龄等"
        />
      </van-cell-group>
      <div class="submit">
        <p class="total">
          合计 <span class="total-price">¥{{ total }}</span>
        </p>
        <van-button
          type="primary"
          block
          native-type="submit"
          :loading="submitting"
        >
          提交预约
        </van-button>
      </div>
    </van-form>
  </van-popup>
</template>

<style scoped>
.dialog {
  width: min(88vw, 340px);
  background: var(--color-surface);
}

.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-md) 0;
}

.head-title {
  font-size: var(--font-size-lg);
}

.head-session {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.head-close {
  flex: 0 0 auto;
  margin: 0;
  padding: 0 var(--space-xs);
  font-size: 22px;
  line-height: 1;
  color: var(--color-ink-muted);
  background: none;
  border: none;
}

.form {
  margin-top: var(--space-sm);
}

.notice {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  margin: 0 var(--space-md) var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-sm);
  color: var(--color-pine);
  background: color-mix(in srgb, var(--color-pine) 10%, var(--color-surface));
  border-radius: var(--radius-sm);
}

.notice-text {
  flex: 1;
  min-width: 0;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-link {
  flex: 0 0 auto;
  margin: 0;
  padding: 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-pine);
  background: none;
  border: none;
}

.group {
  margin: 0;
}

.submit {
  padding: var(--space-md);
}

.total {
  display: flex;
  align-items: baseline;
  justify-content: flex-end;
  gap: var(--space-xs);
  margin: 0 0 var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.total-price {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--color-cinnabar);
}
</style>
