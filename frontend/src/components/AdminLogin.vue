<template>
  <div class="login-shell">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <p class="eyebrow">Admin Access</p>
          <h2>{{ ROOM_LABEL }}管理后台</h2>
          <p>使用管理员账号登录后即可审批预约。若忘记密码，请在 Render 中重置 `ADMIN_PASSWORD`。</p>
        </div>
      </template>

      <el-form label-position="top" @submit.prevent="login">
        <el-form-item label="管理员账号">
          <el-input v-model.trim="form.username" placeholder="请输入管理员账号" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            @keyup.enter="login"
          />
        </el-form-item>

        <el-alert
          v-if="errorMessage"
          :title="errorMessage"
          type="error"
          show-icon
          :closable="false"
        />

        <el-button type="primary" :loading="loading" class="submit-btn" @click="login">
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { bookingAPI } from '../api/booking'
import { ROOM_LABEL } from '../utils/helpers'

const emit = defineEmits(['login-success'])

const form = reactive({
  username: 'zy',
  password: ''
})

const loading = ref(false)
const errorMessage = ref('')

const login = async () => {
  if (!form.username || !form.password) {
    ElMessage.error('请输入用户名和密码')
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const result = await bookingAPI.adminLogin(form.username, form.password)
    localStorage.setItem('admin_token', result.token)
    ElMessage.success('登录成功')
    emit('login-success')
  } catch (error) {
    errorMessage.value = error.response?.data?.error || '登录失败，请检查账号和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-shell {
  padding-top: 16px;
}

.login-card {
  max-width: 540px;
  margin: 0 auto;
  border: none;
  border-radius: 28px;
  box-shadow: 0 28px 60px rgba(16, 32, 39, 0.12);
}

.login-header {
  display: grid;
  gap: 8px;
}

.login-header h2 {
  margin: 0;
  color: #102027;
}

.login-header p:last-child {
  margin: 0;
  color: #5a6f78;
  line-height: 1.7;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #176b5f;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
}
</style>
