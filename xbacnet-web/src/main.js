/**
 * XBACnet Web Management Interface
 * Main entry point for Vue3 application
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// Internationalization
// import i18n from './i18n'

// Global styles
import './assets/styles/main.scss'

// Create Vue app
const app = createApp(App)

// Register Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Use plugins
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)
// app.use(i18n)

// Initialize authentication state
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initAuth()

// Mount app
app.mount('#app')
