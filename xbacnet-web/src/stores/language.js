/**
 * Language Store
 * Manages application language state
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { availableLanguages } from '@/i18n'

export const useLanguageStore = defineStore('language', () => {
  // State
  const currentLanguage = ref(localStorage.getItem('language') || 'en')
  
  // Actions
  function setLanguage(locale) {
    currentLanguage.value = locale
    localStorage.setItem('language', locale)
    
    // Update i18n locale if available
    try {
      const { locale: i18nLocale } = useI18n()
      i18nLocale.value = locale
    } catch (error) {
      console.warn('I18n not available:', error)
    }
  }
  
  // Initialize language from localStorage
  function initLanguage() {
    const savedLanguage = localStorage.getItem('language') || 'en'
    setLanguage(savedLanguage)
  }
  
  function getAvailableLanguages() {
    return availableLanguages
  }
  
  return {
    // State
    currentLanguage,
    
    // Actions
    setLanguage,
    getAvailableLanguages,
    initLanguage
  }
})
