import axios from 'axios'

const trimTrailingSlash = (value) => value.replace(/\/+$/, '')
const DEPLOYMENT_API_MAP = {
  'meetroom-gamma.vercel.app': 'https://meetroom-px0x.onrender.com',
  'www.meetroom-gamma.vercel.app': 'https://meetroom-px0x.onrender.com'
}

const getApiBaseUrl = () => {
  const envValue = import.meta.env.VITE_API_BASE_URL
  if (envValue) {
    return trimTrailingSlash(envValue)
  }

  if (typeof window !== 'undefined') {
    const runtimeValue = window.__APP_API_BASE_URL__
    if (runtimeValue) {
      return trimTrailingSlash(runtimeValue)
    }

    const { hostname, origin } = window.location
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:5000'
    }

    if (DEPLOYMENT_API_MAP[hostname]) {
      return DEPLOYMENT_API_MAP[hostname]
    }

    if (hostname.endsWith('.onrender.com')) {
      return trimTrailingSlash(origin)
    }
  }

  return ''
}

const client = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
    }
    return Promise.reject(error)
  }
)

export default client
