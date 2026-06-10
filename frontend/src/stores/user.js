import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.is_staff || false)

  async function login(username, password) {
    const res = await api.post('/users/login/', { username, password })
    token.value = res.data.access
    refreshToken.value = res.data.refresh
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('refreshToken', res.data.refresh)
    await fetchProfile()
  }

  async function register(data) {
    await api.post('/users/register/', data)
  }

  async function fetchProfile() {
    const res = await api.get('/users/profile/')
    userInfo.value = res.data
    localStorage.setItem('userInfo', JSON.stringify(res.data))
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
  }

  return { token, refreshToken, userInfo, isLoggedIn, isAdmin, login, register, fetchProfile, logout }
})
