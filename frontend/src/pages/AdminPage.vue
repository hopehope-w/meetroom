<template>
  <section class="admin-page">
    <AdminLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

    <div v-else class="admin-layout">
      <section class="admin-hero">
        <div>
          <p class="eyebrow">Admin Console</p>
          <h2>{{ ROOM_LABEL }}审批后台</h2>
          <p>集中处理待审批预约，快速查看近期排期和当前数据库状态。</p>
        </div>

        <div class="admin-summary">
          <div class="admin-summary__card">
            <span>登录状态</span>
            <strong>已验证</strong>
          </div>
          <div class="admin-summary__card">
            <span>密码管理</span>
            <strong>通过 Render 环境变量重置</strong>
          </div>
        </div>

        <el-button type="danger" plain @click="logout">退出登录</el-button>
      </section>

      <AdminStats />
      <AdminApproval />
      <AdminDatabase />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import AdminApproval from '../components/AdminApproval.vue'
import AdminDatabase from '../components/AdminDatabase.vue'
import AdminLogin from '../components/AdminLogin.vue'
import AdminStats from '../components/AdminStats.vue'
import { ROOM_LABEL } from '../utils/helpers'

const isLoggedIn = ref(false)

const handleLoginSuccess = () => {
  isLoggedIn.value = true
}

const logout = () => {
  localStorage.removeItem('admin_token')
  isLoggedIn.value = false
}

onMounted(() => {
  isLoggedIn.value = Boolean(localStorage.getItem('admin_token'))
})
</script>

<style scoped>
.admin-layout {
  display: grid;
  gap: 20px;
}

.admin-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 1fr) auto;
  gap: 16px;
  align-items: end;
  padding: 24px 28px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(19, 38, 44, 0.08);
  box-shadow: 0 18px 42px rgba(16, 32, 39, 0.06);
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #176b5f;
}

.admin-hero h2 {
  margin: 0;
  color: #102027;
}

.admin-hero p {
  margin: 10px 0 0;
  color: #5a6f78;
}

.admin-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.admin-summary__card {
  padding: 16px 18px;
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(243, 248, 250, 0.95), rgba(235, 243, 247, 0.95));
}

.admin-summary__card span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #5a6f78;
}

.admin-summary__card strong {
  color: #102027;
}

@media (max-width: 960px) {
  .admin-hero {
    grid-template-columns: 1fr;
    align-items: stretch;
  }

  .admin-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-hero {
    padding: 20px 18px;
  }
}
</style>
