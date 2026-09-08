<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { logout } from './api/auth'
import { currentStaff } from './session'

const route = useRoute()
const router = useRouter()
const isLogin = computed(() => route.path === '/login')

const onLogout = async () => {
  await logout()
  currentStaff.value = null
  await router.push('/login')
}
</script>

<template>
  <el-container v-if="!isLogin" class="shell">
    <el-header class="header">
      <div class="brand">
        <strong>营地预约后台</strong>
        <span v-if="currentStaff" class="camp">{{ currentStaff.camp_name }}</span>
      </div>
      <div class="account">
        <span v-if="currentStaff">{{ currentStaff.username }}</span>
        <el-button text type="primary" @click="onLogout">退出</el-button>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px" class="aside">
        <el-menu :default-active="route.path" router>
          <el-menu-item index="/">预约建联</el-menu-item>
          <el-menu-item index="/activities">活动排期</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
  <router-view v-else />
</template>

<style>
html,
body,
#app {
  margin: 0;
  height: 100%;
  font-family:
    system-ui,
    -apple-system,
    'Segoe UI',
    sans-serif;
}

.shell {
  min-height: 100%;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--el-border-color);
}

.brand {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.camp {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.account {
  display: flex;
  align-items: center;
  gap: 8px;
}

.aside {
  border-right: 1px solid var(--el-border-color);
}
</style>
