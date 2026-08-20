<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { showSuccessToast, showToast } from 'vant'

type TokenSwatch = {
  token: string
  name: string
}

const colorTokens: TokenSwatch[] = [
  { token: '--color-bg', name: '宣纸底' },
  { token: '--color-surface', name: '玉白' },
  { token: '--color-ink', name: '墨' },
  { token: '--color-ink-muted', name: '淡墨' },
  { token: '--color-pine', name: '松绿' },
  { token: '--color-pine-deep', name: '松绿深' },
  { token: '--color-moss', name: '苔' },
  { token: '--color-cinnabar', name: '朱砂' },
  { token: '--color-line', name: '绢色线' },
  { token: '--color-on-primary', name: '主色上的字' },
]

const spaceTokens: TokenSwatch[] = [
  { token: '--space-base', name: 'base' },
  { token: '--space-xs', name: 'xs' },
  { token: '--space-sm', name: 'sm' },
  { token: '--space-md', name: 'md' },
  { token: '--space-lg', name: 'lg' },
  { token: '--space-xl', name: 'xl' },
]

const radiusTokens: TokenSwatch[] = [
  { token: '--radius-sm', name: 'sm' },
  { token: '--radius-md', name: 'md' },
  { token: '--radius-lg', name: 'lg' },
]

const resolved = ref<Record<string, string>>({})
const phone = ref('')

onMounted(() => {
  const styles = getComputedStyle(document.documentElement)
  const next: Record<string, string> = {}
  for (const item of [...colorTokens, ...spaceTokens, ...radiusTokens]) {
    next[item.token] = styles.getPropertyValue(item.token).trim()
  }
  resolved.value = next
})

const goHome = () => {
  window.location.href = '/'
}

const onToast = () => {
  showToast('松绿主题已生效')
}

const onSuccess = () => {
  showSuccessToast('操作成功')
}
</script>

<template>
  <div class="ab-page">
    <van-nav-bar
      title="样式系统"
      left-text="首页"
      left-arrow
      safe-area-inset-top
      @click-left="goHome"
    />

    <div class="body">
      <section class="section">
        <h2 class="ab-title section-title">颜色</h2>
        <div class="swatches">
          <div v-for="item in colorTokens" :key="item.token" class="swatch">
            <div class="swatch-chip" :style="{ background: `var(${item.token})` }" />
            <p class="swatch-name">{{ item.name }}</p>
            <p class="swatch-meta">{{ item.token }}</p>
            <p class="swatch-meta">{{ resolved[item.token] }}</p>
          </div>
        </div>
      </section>

      <section class="section">
        <h2 class="ab-title section-title">字体</h2>
        <p class="type-title">页标题 · 黑体栈</p>
        <p class="type-sans">正文说明 · 同样是系统黑体。</p>
      </section>

      <section class="section">
        <h2 class="ab-title section-title">间距</h2>
        <div v-for="item in spaceTokens" :key="item.token" class="space-row">
          <span class="space-label">{{ item.name }}</span>
          <span class="space-bar" :style="{ width: `var(${item.token})` }" />
          <span class="space-value">{{ resolved[item.token] }}</span>
        </div>
      </section>

      <section class="section">
        <h2 class="ab-title section-title">圆角</h2>
        <div class="radius-row">
          <div
            v-for="item in radiusTokens"
            :key="item.token"
            class="radius-card"
            :style="{ borderRadius: `var(${item.token})` }"
          >
            {{ item.name }}
            <small>{{ resolved[item.token] }}</small>
          </div>
        </div>
      </section>

      <section class="section">
        <h2 class="ab-title section-title">Vant</h2>
        <div class="stack">
          <van-button type="primary" block @click="onToast">主按钮 松绿</van-button>
          <van-button type="success" block @click="onSuccess">成功 苔绿</van-button>
          <van-button block>默认</van-button>
          <van-button type="danger" block>危险 朱砂</van-button>
        </div>

        <van-cell-group inset class="group">
          <van-cell title="活动名称" value="松间夜读" />
          <van-cell title="名额" value="12 / 20" is-link @click="onToast" />
        </van-cell-group>

        <div class="tags">
          <van-tag type="primary">可预约</van-tag>
          <van-tag type="success">进行中</van-tag>
          <van-tag type="danger">已满</van-tag>
        </div>

        <van-field v-model="phone" label="手机号" placeholder="请输入手机号" />
      </section>
    </div>
  </div>
</template>

<style scoped>
.body {
  padding: var(--space-md);
}

.section {
  margin-bottom: var(--space-xl);
}

.section-title {
  margin-bottom: var(--space-sm);
  font-size: var(--font-size-lg);
}

.swatches {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-sm);
}

.swatch {
  padding: var(--space-sm);
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  border-radius: var(--radius-md);
}

.swatch-chip {
  height: 36px;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-sm);
}

.swatch-name {
  margin: var(--space-xs) 0 0;
  font-size: var(--font-size-md);
}

.swatch-meta {
  margin: 2px 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
  word-break: break-all;
}

.type-title {
  margin: 0 0 var(--space-xs);
  font-family: var(--font-sans);
  font-size: var(--font-size-xl);
  font-weight: 600;
}

.type-sans {
  margin: 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-md);
  color: var(--color-ink-muted);
}

.space-row {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.space-label {
  width: 36px;
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.space-bar {
  height: 8px;
  background: var(--color-pine);
  border-radius: var(--radius-sm);
}

.space-value {
  font-size: var(--font-size-sm);
  color: var(--color-ink-muted);
}

.radius-row {
  display: flex;
  gap: var(--space-sm);
}

.radius-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 72px;
  background: var(--color-surface);
  border: 1px solid var(--color-line);
  font-size: var(--font-size-sm);
}

.radius-card small {
  color: var(--color-ink-muted);
}

.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.group {
  margin: var(--space-md) 0;
}

.tags {
  display: flex;
  gap: var(--space-xs);
  margin-bottom: var(--space-md);
}
</style>
