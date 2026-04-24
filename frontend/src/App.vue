<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="brand">
        <span class="brand-kicker">Meeting Booking</span>
        <h1>211 会议室预约</h1>
      </div>
      <nav class="nav">
        <router-link to="/" class="nav-link">预约</router-link>
        <router-link to="/admin" class="nav-link">管理后台</router-link>
      </nav>
    </header>

    <main class="app-main">
      <router-view />
    </main>

    <Notification
      :show="notificationStore.show"
      :message="notificationStore.message"
      :type="notificationStore.type"
    />
  </div>
</template>

<script setup>
import Notification from './components/Notification.vue'
import { useNotificationStore } from './stores/notification'

const notificationStore = useNotificationStore()
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(13, 148, 136, 0.18), transparent 28%),
    radial-gradient(circle at bottom right, rgba(14, 116, 144, 0.16), transparent 30%),
    linear-gradient(180deg, #f6fbfb 0%, #edf4f7 100%);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  padding: 24px 32px;
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(248, 250, 252, 0.82);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 30;
}

.brand h1 {
  margin: 4px 0 0;
  font-size: 28px;
  line-height: 1.1;
  color: #0f172a;
}

.brand-kicker {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #0f766e;
}

.nav {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.nav-link {
  padding: 10px 14px;
  border-radius: 999px;
  color: #0f172a;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(15, 23, 42, 0.08);
  transition: all 0.2s ease;
}

.nav-link.router-link-active {
  color: #ffffff;
  background: linear-gradient(135deg, #0f766e 0%, #0f4c81 100%);
  border-color: transparent;
}

.app-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 28px 24px 40px;
}

@media (max-width: 768px) {
  .app-header {
    align-items: stretch;
    flex-direction: column;
    padding: 20px 18px;
  }

  .brand h1 {
    font-size: 24px;
  }

  .app-main {
    padding: 20px 14px 32px;
  }
}
</style>
