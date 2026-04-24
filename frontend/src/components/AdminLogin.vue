<template>
  <div class="login-shell">
    <section class="login-hero">
      <div class="login-hero__copy">
        <p class="eyebrow">Admin Access</p>
        <h2>{{ ROOM_LABEL }}管理后台</h2>
        <p>轻量处理待审批预约，快速查看近期排期。忘记密码时，通过 Render 环境变量重置即可。</p>
      </div>

      <div class="login-hero__tips">
        <div class="tip-card">
          <span>适合场景</span>
          <strong>快速审批与巡检</strong>
        </div>
        <div class="tip-card">
          <span>密码恢复</span>
          <strong>重置 `ADMIN_PASSWORD`</strong>
        </div>
      </div>
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
  display: grid;
  gap: 18px;
  padding-top: 6px;
}

.login-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.9fr);
  gap: 18px;
  padding: 28px;
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(16, 33, 39, 0.95) 0%, rgba(24, 86, 80, 0.88) 100%);
  box-shadow: 0 24px 56px rgba(16, 32, 39, 0.16);
  color: #fff;
}

.login-hero__copy {
  display: grid;
  gap: 10px;
}

.login-hero__copy h2 {
  margin: 0;
  font-size: 34px;
  line-height: 1.08;
}

.login-hero__copy p:last-child {
  margin: 0;
  max-width: 620px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.84);
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

.login-hero__tips {
  display: grid;
  gap: 12px;
}

.tip-card {
  padding: 18px 20px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
}

.tip-card span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.68);
}

.tip-card strong {
  color: #fff;
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

@media (max-width: 900px) {
  .login-hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .login-hero {
    padding: 22px 18px;
  }

  .login-hero__copy h2 {
    font-size: 28px;
  }
}
</style>
