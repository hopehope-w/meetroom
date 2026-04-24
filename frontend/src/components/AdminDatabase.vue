<template>
  <el-card class="admin-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">Data Status</p>
          <h3>数据库概览</h3>
        </div>
        <el-space wrap>
          <el-button type="primary" plain :loading="loadingInfo" @click="refreshInfo">刷新</el-button>
          <el-button type="danger" :loading="loadingCleanup" @click="cleanup">清理旧数据</el-button>
        </el-space>
      </div>
    </template>

    <div class="database-banner">
      <span>当前存储</span>
      <strong>SQLite</strong>
      <p>当前版本仍保持轻量存储。数据库持久化问题已确认为后续改进项，本轮界面不再扩展复杂说明。</p>
    </div>

    <el-skeleton v-if="loadingInfo" :rows="4" animated />

    <div v-else class="stats-grid">
      <el-statistic title="总预约数" :value="dbInfo.total_bookings" />
      <el-statistic title="最近一周" :value="dbInfo.recent_week" />
      <el-statistic title="最近一月" :value="dbInfo.recent_month" />
      <el-statistic title="30 天前数据" :value="dbInfo.old_data_count" />
    </div>

    <el-alert
      v-if="dbInfo.cleanup_threshold"
      :title="dbInfo.cleanup_threshold"
      type="info"
      show-icon
      :closable="false"
      class="top-gap"
    />

    <el-alert
      v-if="cleanupResult"
      :title="cleanupResult"
      :type="cleanupSuccess ? 'success' : 'error'"
      show-icon
      :closable="false"
      class="top-gap"
    />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { bookingAPI } from '../api/booking'
import { useNotificationStore } from '../stores/notification'

const notification = useNotificationStore()

const dbInfo = ref({
  total_bookings: 0,
  recent_week: 0,
  recent_month: 0,
  old_data_count: 0,
  cleanup_threshold: ''
})

const loadingInfo = ref(false)
const loadingCleanup = ref(false)
const cleanupResult = ref('')
const cleanupSuccess = ref(false)

const refreshInfo = async () => {
  loadingInfo.value = true
  try {
    dbInfo.value = await bookingAPI.getDatabaseInfo()
  } catch (error) {
    notification.showNotification('加载数据库信息失败', 'error')
  } finally {
    loadingInfo.value = false
  }
}

const cleanup = async () => {
  try {
    await ElMessageBox.confirm('确认要清理 30 天前的历史预约数据吗？', '清理确认', {
      type: 'warning',
      confirmButtonText: '确认',
      cancelButtonText: '取消'
    })

    loadingCleanup.value = true
    const result = await bookingAPI.cleanup()
    cleanupSuccess.value = true
    cleanupResult.value = result.message || '清理完成'
    notification.showNotification('历史数据清理完成', 'success')
    await refreshInfo()
  } catch (error) {
    if (error !== 'cancel') {
      cleanupSuccess.value = false
      cleanupResult.value = '清理失败，请稍后重试'
      notification.showNotification(cleanupResult.value, 'error')
    }
  } finally {
    loadingCleanup.value = false
  }
}

onMounted(() => {
  refreshInfo()
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

.database-banner {
  margin-bottom: 18px;
  padding: 18px 20px;
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(242, 246, 249, 0.95), rgba(236, 243, 247, 0.95));
}

.database-banner span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #5a6f78;
}

.database-banner strong {
  display: block;
  margin-bottom: 8px;
  font-size: 24px;
  color: #102027;
}

.database-banner p {
  margin: 0;
  line-height: 1.7;
  color: #5a6f78;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.top-gap {
  margin-top: 16px;
}

@media (max-width: 960px) {
  .card-header {
    flex-direction: column;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
