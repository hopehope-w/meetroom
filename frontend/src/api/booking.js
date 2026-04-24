import client from './client'

export const bookingAPI = {
  create(data) {
    return client.post('/api/bookings', data)
  },

  getAll(params) {
    return client.get('/api/bookings', { params })
  },

  getMyBookings(params) {
    return client.get('/api/my-bookings', { params })
  },

  checkConflict(params) {
    return client.get('/api/availability', { params })
  },

  getStats() {
    return client.get('/api/stats')
  },

  updateStatus(bookingId, status) {
    return client.put(`/api/bookings/${bookingId}`, { status })
  },

  getDatabaseInfo() {
    return client.get('/api/database-info')
  },

  cleanup() {
    return client.post('/api/cleanup')
  },

  adminLogin(username, password) {
    return client.post('/api/login', { username, password })
  }
}
