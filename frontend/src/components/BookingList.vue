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

    <div class="summary-strip">
      <div>
        <span>房间</span>
        <strong>{{ ROOM_LABEL }}</strong>
      </div>
      <div>
        <span>可见范围</span>
        <strong>未来 30 天</strong>
      </div>
      <div>
        <span>当前记录</span>
        <strong>{{ bookings.length }} 条</strong>
      </div>
    </div>

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
import { formatDateTime, getStatusLabel, getStatusType, ROOM_LABEL } from '../utils/helpers'

const bookings = ref([])
const loading = ref(false)

let pollTimer = null

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
  border-radius: 26px;
  box-shadow: 0 24px 54px rgba(16, 32, 39, 0.08);
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
  color: #176b5f;
}

h2 {
  margin: 0;
  font-size: 22px;
  color: #102027;
}

.summary-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.summary-strip > div {
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(243, 247, 249, 0.92);
}

.summary-strip span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #5a6f78;
}

.summary-strip strong {
  color: #102027;
}

.booking-list {
  display: grid;
  gap: 14px;
}

.booking-item {
  padding: 18px;
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(241, 247, 249, 0.94));
  border: 1px solid rgba(19, 38, 44, 0.06);
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
  color: #102027;
}

.booking-item p {
  margin: 6px 0 0;
  color: #5a6f78;
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
  color: #176b5f;
}

.meta-grid dd {
  margin: 6px 0 0;
  color: #102027;
}

@media (max-width: 768px) {
  .summary-strip,
  .meta-grid {
    grid-template-columns: 1fr;
  }

  .booking-item__top,
  .card-header {
    flex-direction: column;
  }
}
</style>
