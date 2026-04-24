<template>
  <Transition name="notification">
    <div v-if="show" :class="['notification', type]">
      {{ message }}
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'info'
  },
  show: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  max-width: 320px;
  padding: 14px 18px;
  border-radius: 14px;
  color: #fff;
  font-weight: 600;
  z-index: 1000;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
}

.notification.success {
  background: #059669;
}

.notification.error {
  background: #dc2626;
}

.notification.info {
  background: #2563eb;
}

.notification.warning {
  background: #d97706;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.25s ease;
}

.notification-enter-from,
.notification-leave-to {
  transform: translateX(24px);
  opacity: 0;
}
</style>
