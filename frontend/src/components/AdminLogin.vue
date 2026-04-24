<template>
  <el-card class="login-card">
    <template #header>
      <div class="login-header">
        <p class="eyebrow">Admin Access</p>
        <h2>管理员登录</h2>
      </div>
    </template>

    <el-form label-position="top" @submit.prevent="login">
      <el-form-item label="用户名">
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
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { bookingAPI } from '../api/booking'

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
    errorMessage.value = error.response?.data?.error || '登录失败，请检查账号密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-card {
  max-width: 460px;
  margin: 48px auto 0;
  border: none;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.1);
}

.login-header h2 {
  margin: 0;
  color: #0f172a;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #0f766e;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
}
</style>
