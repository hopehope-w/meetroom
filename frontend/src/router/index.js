import { createRouter, createWebHistory } from 'vue-router'
import BookingPage from '../pages/BookingPage.vue'
import AdminPage from '../pages/AdminPage.vue'
import { appMeta } from '../utils/theme'

const routes = [
  {
    path: '/',
    name: 'Booking',
    component: BookingPage,
    meta: { title: appMeta.bookingPageTitle }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminPage,
    meta: { title: appMeta.adminPageTitle }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || appMeta.title
  next()
})

export default router
