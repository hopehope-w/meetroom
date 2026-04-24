<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="brand">
        <span class="brand-kicker">Room Booking</span>
        <h1>{{ appMeta.shortTitle }}</h1>
        <p>轻量、高效、可直接落地的会议预约入口。</p>
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
import { appMeta } from './utils/theme'

const notificationStore = useNotificationStore()
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(180, 227, 255, 0.55), transparent 24%),
    radial-gradient(circle at 85% 15%, rgba(151, 206, 192, 0.4), transparent 18%),
    linear-gradient(180deg, #f7f4ec 0%, #eef3f8 46%, #f4f8fb 100%);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  padding: 24px 32px;
  border-bottom: 1px solid rgba(19, 38, 44, 0.08);
  background: rgba(247, 244, 236, 0.8);
  backdrop-filter: blur(14px);
}

.brand {
  display: grid;
  gap: 6px;
}

.brand-kicker {
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #176b5f;
}

.brand h1 {
  margin: 0;
  font-size: 30px;
  line-height: 1.08;
  color: #102027;
}

.brand p {
  margin: 0;
  color: #47616d;
}

.nav {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.nav-link {
  padding: 10px 16px;
  border-radius: 999px;
  color: #102027;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.64);
  border: 1px solid rgba(19, 38, 44, 0.08);
  transition: all 0.2s ease;
}

.nav-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(16, 32, 39, 0.08);
}

.nav-link.router-link-active {
  color: #fff;
  background: linear-gradient(135deg, #155b56 0%, #234c7c 100%);
  border-color: transparent;
}

.app-main {
  max-width: 1240px;
  margin: 0 auto;
  padding: 28px 24px 40px;
}

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 18px;
  }

  .brand h1 {
    font-size: 26px;
  }

  .app-main {
    padding: 20px 14px 32px;
  }
}
</style>
