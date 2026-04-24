<template>
  <section class="admin-page">
    <AdminLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

    <div v-else class="admin-layout">
      <section class="admin-hero">
        <div>
          <p class="eyebrow">Admin Console</p>
          <h2>{{ ROOM_LABEL }}审批后台</h2>
          <p>集中处理待审批预约，快速查看近期排期和当前系统状态。</p>
        </div>

        <el-button type="danger" plain @click="logout">退出登录</el-button>
      </section>

      <div class="admin-grid">
        <section class="admin-grid__main">
          <AdminApproval />
          <AdminStats />
        </section>

        <aside class="admin-grid__side">
          <div class="side-note">
            <p class="side-note__label">后续改进计划</p>
            <h3>数据持久化</h3>
            <p>当前数据无法稳定持久化保存，根因在 SQLite 部署形态。页面先保持轻量，后续再迁移至 PostgreSQL。</p>
          </div>
          <AdminDatabase />
        </aside>
      </div>
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
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
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

.admin-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(300px, 0.92fr);
  gap: 20px;
  align-items: start;
}

.admin-grid__main,
.admin-grid__side {
  display: grid;
  gap: 20px;
  min-width: 0;
}

.side-note {
  padding: 20px 22px;
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(244, 246, 240, 0.96), rgba(239, 243, 235, 0.96));
  border: 1px solid rgba(78, 103, 73, 0.08);
  box-shadow: 0 16px 34px rgba(16, 32, 39, 0.05);
}

.side-note__label {
  margin: 0 0 10px;
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #4f6d53;
}

.side-note h3 {
  margin: 0 0 10px;
  color: #102027;
}

.side-note p:last-child {
  margin: 0;
  line-height: 1.7;
  color: #5a6f78;
}

@media (max-width: 1100px) {
  .admin-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-hero {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 18px;
  }

  .side-note {
    padding: 18px;
  }
}
</style>
