import { createRouter, createWebHistory } from 'vue-router'
import BookingPage from '../pages/BookingPage.vue'
import AdminPage from '../pages/AdminPage.vue'

const routes = [
  {
    path: '/',
    name: 'Booking',
    component: BookingPage,
    meta: { title: '会议室预约' }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { title: '管理员后台' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '会议室预约'} - 211 会议室`
  next()
})

export default router
