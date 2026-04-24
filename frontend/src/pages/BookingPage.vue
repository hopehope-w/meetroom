<template>
  <section class="booking-page">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Meeting Space</p>
        <h2>{{ ROOM_LABEL }}预约</h2>
        <p>
          面向团队日常协作的轻量预约页面。直接提交申请，管理员确认后即可安排使用，页面只保留必要信息和当前排期。
        </p>
      </div>

      <div class="hero-panel">
        <div class="hero-panel__item">
          <span>房间</span>
          <strong>{{ ROOM_LABEL }}</strong>
        </div>
        <div class="hero-panel__item">
          <span>状态</span>
          <strong>提交后进入审批</strong>
        </div>
      </div>
    </section>

    <section class="booking-layout">
      <div class="booking-layout__form">
        <BookingForm />
      </div>
      <div class="booking-layout__list">
        <BookingList />
      </div>
    </section>
  </section>
</template>

<script setup>
import BookingForm from '../components/BookingForm.vue'
import BookingList from '../components/BookingList.vue'
import { ROOM_LABEL } from '../utils/helpers'
</script>

<style scoped>
.booking-page {
  display: grid;
  gap: 22px;
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(250px, 0.75fr);
  gap: 20px;
  padding: 32px;
  border-radius: 30px;
  background:
    linear-gradient(135deg, rgba(17, 77, 70, 0.96) 0%, rgba(34, 70, 118, 0.94) 100%);
  box-shadow: 0 24px 56px rgba(21, 74, 94, 0.22);
  color: #fff;
  overflow: hidden;
}

.hero-copy {
  display: grid;
  gap: 12px;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.72);
}

.hero h2 {
  margin: 0;
  font-size: 40px;
  line-height: 1.08;
}

.hero p {
  margin: 0;
  max-width: 700px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.88);
}

.hero-panel {
  display: grid;
  gap: 14px;
  align-self: center;
}

.hero-panel__item {
  padding: 20px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(10px);
}

.hero-panel__item span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.72);
}

.hero-panel__item strong {
  font-size: 20px;
  font-weight: 600;
}

.booking-layout {
  display: grid;
  grid-template-columns: minmax(320px, 0.95fr) minmax(0, 1.4fr);
  gap: 20px;
  align-items: start;
}

.booking-layout__form,
.booking-layout__list {
  min-width: 0;
}

@media (max-width: 960px) {
  .hero,
  .booking-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 24px 18px;
  }

  .hero h2 {
    font-size: 30px;
  }
}
</style>
