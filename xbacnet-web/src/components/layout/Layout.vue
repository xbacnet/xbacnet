<template>
  <div class="layout">
    <!-- Sidebar Navigation -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <Sidebar />
    </el-aside>
    
    <!-- Main Content -->
    <el-container>
      <!-- Header -->
      <el-header class="header">
        <Header />
      </el-header>
      
      <!-- Main Content Area -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

const appStore = useAppStore()

const sidebarWidth = computed(() => {
  return appStore.sidebarCollapsed ? '64px' : '240px'
})
</script>

<style lang="scss" scoped>
.layout {
  height: 100vh;
  display: flex;
}

.sidebar {
  background-color: var(--sidebar-bg);
  transition: width 0.3s;
  overflow: hidden;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.header {
  background-color: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 0;
  height: 60px;
  line-height: 60px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.main-content {
  background-color: var(--main-bg);
  padding: 20px;
  overflow-y: auto;
  min-height: calc(100vh - 60px);
}
</style>
