<template>
  <section class="booking-page">
    <div class="hero">
      <div>
        <p class="eyebrow">Lightweight Scheduling</p>
        <h2>先把预约、审批和通知跑通</h2>
        <p class="hero-copy">
          这是面向 211 会议室的轻量级预约入口。当前版本优先保证流程闭环：提交预约、
          管理员审批、飞书群通知和线上可访问。
        </p>
      </div>
      <div class="hero-badge">Vercel + Render + SQLite</div>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="9">
        <BookingForm />
      </el-col>
      <el-col :xs="24" :lg="15">
        <BookingList />
      </el-col>
    </el-row>
  </section>
</template>

<script setup>
import BookingForm from '../components/BookingForm.vue'
import BookingList from '../components/BookingList.vue'
</script>

<style scoped>
.booking-page {
  display: grid;
  gap: 20px;
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  padding: 28px;
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(15, 118, 110, 0.92) 0%, rgba(14, 116, 144, 0.9) 100%),
    #0f766e;
  color: #ffffff;
  box-shadow: 0 24px 50px rgba(15, 118, 110, 0.22);
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.78);
}

.hero h2 {
  margin: 0;
  font-size: 32px;
  line-height: 1.15;
}

.hero-copy {
  max-width: 720px;
  margin: 14px 0 0;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.88);
}

.hero-badge {
  align-self: flex-start;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.2);
  white-space: nowrap;
}

@media (max-width: 768px) {
  .hero {
    padding: 22px 18px;
    flex-direction: column;
  }

  .hero h2 {
    font-size: 26px;
  }
}
</style>
