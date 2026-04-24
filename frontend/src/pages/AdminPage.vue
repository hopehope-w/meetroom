<template>
  <section class="admin-page">
    <AdminLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

    <div v-else class="admin-layout">
      <section class="admin-toolbar">
        <div>
          <p class="eyebrow">Admin Console</p>
          <h2>预约审批后台</h2>
        </div>
        <el-button type="danger" @click="logout">退出登录</el-button>
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

.admin-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-end;
  padding: 24px 28px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #0f766e;
}

h2 {
  margin: 0;
  color: #0f172a;
}

@media (max-width: 768px) {
  .admin-toolbar {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 18px;
  }
}
</style>
