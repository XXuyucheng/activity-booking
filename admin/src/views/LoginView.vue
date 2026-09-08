<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'
import { ApiError } from '../api/http'
import { currentStaff } from '../session'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
})

const onSubmit = async () => {
  if (!form.username.trim() || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    currentStaff.value = await login(form.username, form.password)
    await router.push('/')
  } catch (error) {
    const message = error instanceof ApiError ? '用户名或密码错误' : '登录失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login">
    <el-card class="card" shadow="never">
      <h1>员工登录</h1>
      <p class="hint">账号密码登录，不走微信</p>
      <el-form @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" autocomplete="username" />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            show-password
            autocomplete="current-password"
            @keyup.enter="onSubmit"
          />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%">
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}

.card {
  width: 360px;
}

h1 {
  margin: 0 0 8px;
  font-size: 22px;
}

.hint {
  margin: 0 0 20px;
  color: var(--el-text-color-secondary);
}
</style>
