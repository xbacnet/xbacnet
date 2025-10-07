/**
 * Authentication Store
 * Manages user authentication state
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(false)

  // Getters
  const currentUser = computed(() => user.value)
  const isLoggedIn = computed(() => isAuthenticated.value && user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  // Actions
  async function login(credentials) {
    try {
      const response = await apiService.login(credentials)

      if (response.success) {
        user.value = response.user
        isAuthenticated.value = true

        // Store token if provided
        if (response.token) {
          token.value = response.token
          localStorage.setItem('token', response.token)
        } else {
          // If no token provided, store user data to maintain session
          localStorage.setItem('user', JSON.stringify(response.user))
        }

        return { success: true, user: response.user }
      } else {
        return { success: false, error: response.error }
      }
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      }
    }
  }

  async function logout() {
    try {
      if (user.value) {
        await apiService.logout({ user_id: user.value.id })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear authentication state
      user.value = null
      token.value = null
      isAuthenticated.value = false
      localStorage.removeItem('token')
    }
  }

  function setUser(userData) {
    user.value = userData
    isAuthenticated.value = true
  }

  function clearAuth() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Initialize authentication state
  function initAuth() {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    if (storedToken) {
      token.value = storedToken
      // You might want to validate the token here
      // For now, we'll assume it's valid
      isAuthenticated.value = true
    } else if (storedUser) {
      // If no token but user data exists, restore user session
      try {
        user.value = JSON.parse(storedUser)
        isAuthenticated.value = true
      } catch (error) {
        console.error('Error parsing stored user data:', error)
        localStorage.removeItem('user')
        isAuthenticated.value = false
        user.value = null
      }
    } else {
      // Ensure clean state if no token or user data
      isAuthenticated.value = false
      user.value = null
    }
  }

  return {
    // State
    user,
    token,
    isAuthenticated,

    // Getters
    currentUser,
    isLoggedIn,
    isAdmin,

    // Actions
    login,
    logout,
    setUser,
    clearAuth,
    initAuth
  }
})
