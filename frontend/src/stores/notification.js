import { ref } from 'vue'

const show = ref(false)
const message = ref('')
const type = ref('info')

let notificationTimer = null

export function useNotificationStore() {
  const showNotification = (msg, notificationType = 'info', duration = 3000) => {
    message.value = msg
    type.value = notificationType
    show.value = true

    if (notificationTimer) {
      clearTimeout(notificationTimer)
    }

    notificationTimer = setTimeout(() => {
      show.value = false
    }, duration)
  }

  const hideNotification = () => {
    show.value = false
    if (notificationTimer) {
      clearTimeout(notificationTimer)
      notificationTimer = null
    }
  }

  return {
    show,
    message,
    type,
    showNotification,
    hideNotification
  }
}
