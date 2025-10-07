/**
 * Application Store
 * Manages global application state
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const theme = ref('light')
  
  // Getters
  const isSidebarCollapsed = computed(() => sidebarCollapsed.value)
  const isLoading = computed(() => loading.value)
  const currentTheme = computed(() => theme.value)
  
  // Actions
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
  
  function setSidebarCollapsed(collapsed) {
    sidebarCollapsed.value = collapsed
  }
  
  function setLoading(loadingState) {
    loading.value = loadingState
  }
  
  function setTheme(newTheme) {
    theme.value = newTheme
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', newTheme)
  }
  
  return {
    // State
    sidebarCollapsed,
    loading,
    theme,
    
    // Getters
    isSidebarCollapsed,
    isLoading,
    currentTheme,
    
    // Actions
    toggleSidebar,
    setSidebarCollapsed,
    setLoading,
    setTheme
  }
})
