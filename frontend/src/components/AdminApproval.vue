<template>
  <el-card class="admin-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">Approval Queue</p>
          <h3>待审批预约</h3>
        </div>
        <el-button type="primary" plain :loading="loading" @click="refresh">刷新</el-button>
      </div>
    </template>

    <el-skeleton v-if="loading" :rows="4" animated />
    <el-empty v-else-if="pendingBookings.length === 0" description="暂无待审批预约" />

    <el-table v-else :data="pendingBookings" stripe>
      <el-table-column prop="user_name" label="预约人" min-width="110" />
      <el-table-column prop="department" label="部门" min-width="120" />
      <el-table-column label="开始时间" min-width="160">
        <template #default="{ row }">
          {{ formatDateTime(row.start_time) }}
        </template>
      </el-table-column>
      <el-table-column label="结束时间" min-width="160">
        <template #default="{ row }">
          {{ formatDateTime(row.end_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button type="success" size="small" @click="updateStatus(row.id, 'approved')">
              批准
            </el-button>
            <el-button type="danger" size="small" @click="updateStatus(row.id, 'rejected')">
              拒绝
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { bookingAPI } from '../api/booking'
import { useNotificationStore } from '../stores/notification'

const notification = useNotificationStore()
const allBookings = ref([])
const loading = ref(false)

let pollTimer = null

const pendingBookings = computed(() => allBookings.value.filter((booking) => booking.status === 'pending'))

const formatDateTime = (dateString) => dateString.replace('T', ' ').slice(0, 16)

const refresh = async () => {
  loading.value = true
  try {
    allBookings.value = await bookingAPI.getAll()
  } catch (error) {
    notification.showNotification('加载预约列表失败', 'error')
  } finally {
    loading.value = false
  }
}

const updateStatus = async (bookingId, status) => {
  const label = status === 'approved' ? '批准' : '拒绝'

  try {
    await ElMessageBox.confirm(`确认要${label}这条预约吗？`, '审批确认', {
      type: 'warning',
      confirmButtonText: '确认',
      cancelButtonText: '取消'
    })

    await bookingAPI.updateStatus(bookingId, status)
    notification.showNotification(`预约已${label}`, 'success')
    await refresh()
  } catch (error) {
    if (error !== 'cancel') {
      notification.showNotification('审批操作失败', 'error')
    }
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
</style>
