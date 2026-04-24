// 日期格式化工具
export const formatDateTime = (dateString) => {
  return dateString.replace('T', ' ')
}

export const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(today.getDate() + 1)

  const todayStr = today.getFullYear() + '-' +
    String(today.getMonth() + 1).padStart(2, '0') + '-' +
    String(today.getDate()).padStart(2, '0')
  const tomorrowStr = tomorrow.getFullYear() + '-' +
    String(tomorrow.getMonth() + 1).padStart(2, '0') + '-' +
    String(tomorrow.getDate()).padStart(2, '0')

  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  let dayLabel = ''

  if (dateString === todayStr) {
    dayLabel = '今天'
  } else if (dateString === tomorrowStr) {
    dayLabel = '明天'
  } else {
    dayLabel = weekdays[date.getDay()]
  }

  return `${dateString} (${dayLabel})`
}

export const getStatusType = (status) => {
  const typeMap = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status] || 'info'
}

