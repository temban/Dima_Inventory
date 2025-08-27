import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import router from '@/router'

interface LoginData {
  username: string
  password: string
}

interface AuthResponse {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const isAuthenticated = ref(!!token.value)

  const login = async (credentials: LoginData) => {
    try {
      const response = await axios.post('/api/token/', credentials)
      const data: AuthResponse = response.data
      
      token.value = data.access
      isAuthenticated.value = true
      
      localStorage.setItem('token', data.access)
      localStorage.setItem('refresh', data.refresh)
      
      router.push('/')
    } catch (error) {
      throw new Error('Login failed. Please check your credentials.')
    }
  }

  const logout = () => {
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
    router.push('/login')
  }

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh')
      if (!refresh) {
        throw new Error('No refresh token')
      }

      const response = await axios.post('/api/token/refresh/', {
        refresh
      })
      
      const data: AuthResponse = response.data
      token.value = data.access
      localStorage.setItem('token', data.access)
      
      return data.access
    } catch (error) {
      logout()
      throw error
    }
  }

  return {
    token,
    isAuthenticated,
    login,
    logout,
    refreshToken
  }
})