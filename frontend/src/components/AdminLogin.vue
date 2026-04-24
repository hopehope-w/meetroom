<template>
  <div class="login-shell">
    <section class="login-hero">
      <p class="eyebrow">Admin Access</p>
      <h2>{{ ROOM_LABEL }}管理后台</h2>
      <p class="login-copy">登录后可集中处理待审批预约，并查看当前后台状态。</p>
    </section>

    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <p class="eyebrow">Sign In</p>
          <h3>管理员登录</h3>
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
          登录后台
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
  username: '',
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
  display: grid;
  gap: 18px;
  padding-top: 6px;
}

.login-hero {
  display: grid;
  gap: 10px;
  padding: 30px 32px;
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(16, 33, 39, 0.95) 0%, rgba(24, 86, 80, 0.88) 100%);
  box-shadow: 0 24px 56px rgba(16, 32, 39, 0.16);
  color: #fff;
}

.login-hero h2 {
  margin: 0;
  font-size: 34px;
  line-height: 1.08;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #176b5f;
}

.login-hero .eyebrow {
  color: rgba(255, 255, 255, 0.68);
}

.login-copy {
  margin: 0;
  max-width: 620px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.84);
}

.login-card {
  max-width: 640px;
  margin: 0 auto;
  width: 100%;
  border: none;
  border-radius: 28px;
  box-shadow: 0 28px 60px rgba(16, 32, 39, 0.12);
}

.login-header {
  display: grid;
  gap: 8px;
}

.login-header h3 {
  margin: 0;
  color: #102027;
}

.submit-btn {
  width: 100%;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .login-hero {
    padding: 22px 18px;
  }

  .login-hero h2 {
    font-size: 28px;
  }
}
</style>
