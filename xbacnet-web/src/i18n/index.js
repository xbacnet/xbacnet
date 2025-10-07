/**
 * XBACnet Web Management Interface
 * Internationalization Configuration
 */

import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhCN from './locales/zh-CN.json'

// Get saved language from localStorage or default to English
const savedLanguage = localStorage.getItem('language') || 'en'

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: savedLanguage,
  fallbackLocale: 'en',
  messages: {
    en,
    'zh-CN': zhCN
  }
})

export default i18n
