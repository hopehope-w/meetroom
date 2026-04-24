<template>
  <el-card class="admin-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">Ops Snapshot</p>
          <h3>未来 5 个工作日概览</h3>
        </div>
        <el-button type="primary" plain :loading="loading" @click="refreshStats">刷新</el-button>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />

    <div v-else class="stats-wrap">
      <div class="headline-grid">
        <div class="headline-card">
          <span>预约总数</span>
          <strong>{{ statsData.total }}</strong>
        </div>
        <div class="headline-card">
          <span>当前日期</span>
          <strong>{{ statsData.current_info?.current_date || '--' }}</strong>
        </div>
        <div class="headline-card">
          <span>更新时间</span>
          <strong>{{ statsData.current_info?.current_time || '--' }}</strong>
        </div>
      </div>

      <el-table :data="tableRows" stripe>
        <el-table-column prop="date" label="日期" min-width="160">
          <template #default="{ row }">
            {{ formatShortDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="count" label="预约数" width="100" />
        <el-table-column label="详情" min-width="260">
          <template #default="{ row }">
            <div v-if="row.bookings.length === 0" class="muted">暂无预约</div>
            <div v-else class="row-bookings">
              <el-tag
                v-for="booking in row.bookings"
                :key="booking.id"
                :type="getStatusType(booking.status)"
              >
                {{ booking.user_name }} / {{ getStatusLabel(booking.status) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { bookingAPI } from '../api/booking'
import { useNotificationStore } from '../stores/notification'
import { formatShortDate, getStatusLabel, getStatusType } from '../utils/helpers'

const notification = useNotificationStore()

const statsData = ref({
  days: [],
  by_day: {},
  total: 0,
  current_info: null
})

const loading = ref(false)
let pollTimer = null

const tableRows = computed(() =>
  statsData.value.days.map((day) => ({
    date: day,
    count: (statsData.value.by_day[day] || []).length,
    bookings: statsData.value.by_day[day] || []
  }))
)

const refreshStats = async () => {
  loading.value = true
  try {
    statsData.value = await bookingAPI.getStats()
  } catch (error) {
    notification.showNotification('加载统计信息失败', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshStats()
  pollTimer = setInterval(refreshStats, 60000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
})
</script>

<style scoped>
.admin-card {
  border: none;
  border-radius: 26px;
  box-shadow: 0 24px 54px rgba(16, 32, 39, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #176b5f;
}

h3 {
  margin: 0;
  color: #102027;
}

.stats-wrap {
  display: grid;
  gap: 18px;
}

.headline-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.headline-card {
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(243, 247, 249, 0.92);
}

.headline-card span {
  display: block;
  margin-bottom: 10px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #5a6f78;
}

.headline-card strong {
  font-size: 20px;
  color: #102027;
}

.row-bookings {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.muted {
  color: #64748b;
}

@media (max-width: 768px) {
  .headline-grid {
    grid-template-columns: 1fr;
  }
}
</style>
