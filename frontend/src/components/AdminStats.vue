<template>
  <el-card class="admin-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">Ops Snapshot</p>
          <h3>未来 5 个工作日统计</h3>
        </div>
        <el-button type="primary" plain :loading="loading" @click="refreshStats">刷新</el-button>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />

    <div v-else class="stats-wrap">
      <el-alert
        v-if="statsData.current_info"
        :title="`当前日期 ${statsData.current_info.current_date}，更新时间 ${statsData.current_info.current_time}`"
        type="info"
        :closable="false"
        show-icon
      />

      <el-statistic title="预约总数" :value="statsData.total" />

      <el-table :data="tableRows" stripe>
        <el-table-column prop="date" label="日期" min-width="160" />
        <el-table-column prop="count" label="预约数" width="100" />
        <el-table-column label="详情" min-width="240">
          <template #default="{ row }">
            <div v-if="row.bookings.length === 0" class="muted">暂无预约</div>
            <div v-else class="row-bookings">
              <el-tag
                v-for="booking in row.bookings"
                :key="booking.id"
                :type="getStatusType(booking.status)"
              >
                {{ booking.user_name }} / {{ booking.status }}
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

const notification = useNotificationStore()

const statsData = ref({
  days: [],
  by_day: {},
  total: 0,
  current_info: null
})

const loading = ref(false)
let pollTimer = null

const getStatusType = (status) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

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
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
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
  color: #0f766e;
}

h3 {
  margin: 0;
  color: #0f172a;
}

.stats-wrap {
  display: grid;
  gap: 16px;
}

.row-bookings {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.muted {
  color: #64748b;
}
</style>
