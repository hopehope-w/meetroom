<template>
  <el-card class="panel-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">Upcoming Queue</p>
          <h2>未来 30 天预约列表</h2>
        </div>
        <el-button type="primary" plain :loading="loading" @click="refresh">刷新</el-button>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />

    <el-empty v-else-if="bookings.length === 0" description="暂无未来预约" />

    <div v-else class="booking-list">
      <article v-for="booking in bookings" :key="booking.id" class="booking-item">
        <div class="booking-item__top">
          <div>
            <h3>{{ booking.user_name }}</h3>
            <p>{{ booking.department || '未填写部门' }}</p>
          </div>
          <el-tag :type="getStatusType(booking.status)">
            {{ getStatusLabel(booking.status) }}
          </el-tag>
        </div>
        <dl class="meta-grid">
          <div>
            <dt>开始</dt>
            <dd>{{ formatDateTime(booking.start_time) }}</dd>
          </div>
          <div>
            <dt>结束</dt>
            <dd>{{ formatDateTime(booking.end_time) }}</dd>
          </div>
        </dl>
      </article>
    </div>
  </el-card>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { bookingAPI } from '../api/booking'

const bookings = ref([])
const loading = ref(false)

let pollTimer = null

const formatDateTime = (dateString) => dateString.replace('T', ' ').slice(0, 16)

const getStatusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

const getStatusLabel = (status) => {
  if (status === 'approved') return '已批准'
  if (status === 'rejected') return '已拒绝'
  return '待审批'
}

const refresh = async () => {
  loading.value = true
  try {
    const now = new Date()
    const end = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)
    const data = await bookingAPI.getAll({
      start: now.toISOString(),
      end: end.toISOString()
    })

    const currentTime = now.toISOString()
    bookings.value = data.filter((booking) => booking.end_time >= currentTime)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refresh()
  pollTimer = setInterval(refresh, 30000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
})
</script>

<style scoped>
.panel-card {
  border: none;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #0f766e;
}

h2 {
  margin: 0;
  font-size: 22px;
  color: #0f172a;
}

.booking-list {
  display: grid;
  gap: 14px;
}

.booking-item {
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(240, 249, 255, 0.9));
  border: 1px solid rgba(15, 23, 42, 0.06);
}

.booking-item__top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.booking-item h3 {
  margin: 0;
  color: #0f172a;
}

.booking-item p {
  margin: 6px 0 0;
  color: #475569;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 0;
}

.meta-grid dt {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0f766e;
}

.meta-grid dd {
  margin: 6px 0 0;
  color: #0f172a;
}

@media (max-width: 768px) {
  .meta-grid {
    grid-template-columns: 1fr;
  }

  .booking-item__top,
  .card-header {
    flex-direction: column;
  }
}
</style>
