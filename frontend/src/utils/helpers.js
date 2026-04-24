export const ROOM_LABEL = '207 会议室'
export const ROOM_NUMBER = '207'

const statusTypeMap = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger'
}

const statusLabelMap = {
  pending: '待审批',
  approved: '已批准',
  rejected: '已拒绝'
}

export const formatDateTime = (dateString) => {
  if (!dateString) {
    return '--'
  }

  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) {
    return String(dateString).replace('T', ' ').slice(0, 16)
  }

  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).format(date)
}

export const formatFullDateTime = (dateString) => {
  if (!dateString) {
    return '--'
  }

  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) {
    return String(dateString).replace('T', ' ').slice(0, 16)
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).format(date)
}

export const formatShortDate = (dateString) => {
  if (!dateString) {
    return '--'
  }

  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) {
    return dateString
  }

  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    weekday: 'short'
  }).format(date)
}

export const getStatusType = (status) => statusTypeMap[status] || 'info'

export const getStatusLabel = (status) => statusLabelMap[status] || '未知状态'
