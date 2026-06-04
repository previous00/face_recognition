import { defineStore } from 'pinia'
import { login, register, getProfile, logout } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken,
    isAdmin: (state) => ['admin', 'super_admin'].includes(state.user?.role),
  },
  actions: {
    async login(credentials) {
      const res = await login(credentials)
      this.accessToken = res.data.access
      this.refreshToken = res.data.refresh
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      await this.fetchProfile()
    },
    async register(data) {
      const res = await register(data)
      this.accessToken = res.data.tokens.access
      this.refreshToken = res.data.tokens.refresh
      localStorage.setItem('access_token', res.data.tokens.access)
      localStorage.setItem('refresh_token', res.data.tokens.refresh)
      this.user = res.data.user
    },
    async fetchProfile() {
      const res = await getProfile()
      this.user = res.data
    },
    async logout() {
      try {
        await logout({ refresh: this.refreshToken })
      } catch {}
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})
