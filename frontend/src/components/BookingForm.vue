<template>
  <el-card class="panel-card">
    <template #header>
      <div class="card-header">
        <div>
          <p class="eyebrow">New Request</p>
          <h2>提交预约申请</h2>
        </div>
        <el-tag type="success" effect="dark">{{ ROOM_LABEL }}</el-tag>
      </div>
    </template>

    <div class="panel-intro">
      <p>填写预约人和时间段即可提交申请，系统会先检查冲突，再进入管理员审批。</p>
    </div>

    <el-form label-position="top" class="booking-form" @submit.prevent="submit">
      <el-form-item label="预约人">
        <el-input v-model.trim="form.user_name" placeholder="请输入姓名" clearable />
      </el-form-item>

      <el-form-item label="部门">
        <el-input v-model.trim="form.department" placeholder="请输入部门，可选" clearable />
      </el-form-item>

      <el-form-item label="开始时间">
        <el-date-picker
          v-model="form.start_time"
          type="datetime"
          placeholder="选择开始时间"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DDTHH:mm:ss"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="结束时间">
        <el-date-picker
          v-model="form.end_time"
          type="datetime"
          placeholder="选择结束时间"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DDTHH:mm:ss"
          style="width: 100%"
        />
      </el-form-item>

      <el-alert
        v-if="status.message"
        :title="status.message"
        :type="status.type"
        show-icon
        :closable="true"
        @close="status.message = ''"
      />

      <div class="actions">
        <el-button type="primary" :loading="loading" @click="submit">提交预约</el-button>
        <el-button :loading="loading" @click="checkConflict">检查冲突</el-button>
      </div>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { bookingAPI } from '../api/booking'
import { useNotificationStore } from '../stores/notification'
import { ROOM_LABEL } from '../utils/helpers'

const notification = useNotificationStore()

const form = reactive({
  user_name: '',
  department: '',
  start_time: '',
  end_time: ''
})

const status = reactive({
  message: '',
  type: 'info'
})

const loading = ref(false)

const resetForm = () => {
  form.user_name = ''
  form.department = ''
  form.start_time = ''
  form.end_time = ''
}

const ensureRequiredFields = () => {
  if (!form.user_name || !form.start_time || !form.end_time) {
    ElMessage.error('请填写预约人、开始时间和结束时间')
    return false
  }
  return true
}

const submit = async () => {
  if (!ensureRequiredFields()) {
    return
  }

  loading.value = true
  try {
    await bookingAPI.create({
      user_name: form.user_name,
      department: form.department,
      start_time: form.start_time,
      end_time: form.end_time
    })

    status.message = `${ROOM_LABEL}预约已提交，等待管理员审批`
    status.type = 'success'
    notification.showNotification('预约提交成功，等待审批', 'success')
    resetForm()
  } catch (error) {
    const message = error.response?.data?.error || '提交失败，请稍后重试'
    status.message = message
    status.type = 'error'
    notification.showNotification(message, 'error')
  } finally {
    loading.value = false
  }
}

const checkConflict = async () => {
  if (!form.start_time || !form.end_time) {
    ElMessage.error('请先选择开始和结束时间')
    return
  }

  loading.value = true
  try {
    const result = await bookingAPI.checkConflict({
      start: form.start_time,
      end: form.end_time
    })

    if (result.available) {
      status.message = '当前时间段可预约'
      status.type = 'success'
    } else {
      status.message = '当前时间段已有预约冲突'
      status.type = 'warning'
    }
  } catch (error) {
    status.message = '冲突检查失败，请稍后重试'
    status.type = 'error'
  } finally {
    loading.value = false
  }
}
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

.panel-intro {
  margin-bottom: 18px;
  padding: 14px 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(246, 249, 251, 0.95), rgba(238, 244, 247, 0.95));
}

.panel-intro p {
  margin: 0;
  color: #5a6f78;
  line-height: 1.7;
}

.booking-form {
  display: grid;
  gap: 6px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .actions,
  .card-header {
    flex-direction: column;
  }
}
</style>
