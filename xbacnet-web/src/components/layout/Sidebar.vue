<template>
  <div class="sidebar-container">
    <!-- Logo -->
    <div class="logo">
      <img src="/logo.svg" alt="XBACnet" class="logo-image" v-if="!isCollapsed" />
      <el-icon class="logo-icon" :size="32" v-else><Setting /></el-icon>
      <span v-if="!isCollapsed" class="logo-text">XBACnet</span>
    </div>

    <!-- Navigation Menu -->
    <el-menu
      :default-active="activeMenu"
      :collapse="isCollapsed"
      :unique-opened="true"
      router
      class="sidebar-menu"
      background-color="var(--sidebar-bg)"
      text-color="var(--sidebar-text)"
      active-text-color="var(--sidebar-active)"
    >
      <!-- Dashboard -->
      <el-menu-item index="/dashboard">
        <el-icon><Dashboard /></el-icon>
        <template #title>{{ $t('navigation.dashboard') }}</template>
      </el-menu-item>

      <!-- Analog Objects -->
      <el-sub-menu index="analog">
        <template #title>
          <el-icon><TrendCharts /></el-icon>
          <span>Analog Objects</span>
        </template>
        <el-menu-item index="/analog-inputs">
          <el-icon><DataLine /></el-icon>
          <template #title>{{ $t('navigation.analogInputs') }}</template>
        </el-menu-item>
        <el-menu-item index="/analog-outputs">
          <el-icon><Setting /></el-icon>
          <template #title>{{ $t('navigation.analogOutputs') }}</template>
        </el-menu-item>
        <el-menu-item index="/analog-values">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>{{ $t('navigation.analogValues') }}</template>
        </el-menu-item>
      </el-sub-menu>

      <!-- Binary Objects -->
      <el-sub-menu index="binary">
        <template #title>
          <el-icon><Switch /></el-icon>
          <span>Binary Objects</span>
        </template>
        <el-menu-item index="/binary-inputs">
          <el-icon><Monitor /></el-icon>
          <template #title>Binary Inputs</template>
        </el-menu-item>
        <el-menu-item index="/binary-outputs">
          <el-icon><Operation /></el-icon>
          <template #title>Binary Outputs</template>
        </el-menu-item>
        <el-menu-item index="/binary-values">
          <el-icon><Grid /></el-icon>
          <template #title>Binary Values</template>
        </el-menu-item>
      </el-sub-menu>

      <!-- Multi-state Objects -->
      <el-sub-menu index="multi-state">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>Multi-state Objects</span>
        </template>
        <el-menu-item index="/multi-state-inputs">
          <el-icon><List /></el-icon>
          <template #title>Multi-state Inputs</template>
        </el-menu-item>
        <el-menu-item index="/multi-state-outputs">
          <el-icon><Menu /></el-icon>
          <template #title>Multi-state Outputs</template>
        </el-menu-item>
        <el-menu-item index="/multi-state-values">
          <el-icon><Grid /></el-icon>
          <template #title>Multi-state Values</template>
        </el-menu-item>
      </el-sub-menu>

      <!-- User Management -->
      <el-menu-item index="/users">
        <el-icon><User /></el-icon>
        <template #title>User Management</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const appStore = useAppStore()

const isCollapsed = computed(() => appStore.sidebarCollapsed)
const activeMenu = computed(() => route.path)
</script>

<style lang="scss" scoped>
.sidebar-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-color);
  gap: 10px;

  .logo-image {
    height: 32px;
    width: 32px;
    flex-shrink: 0;
  }

  .logo-icon {
    color: var(--sidebar-text);
    flex-shrink: 0;
  }

  .logo-text {
    color: var(--sidebar-text);
    font-size: 18px;
    font-weight: bold;
    white-space: nowrap;
  }
}

.sidebar-menu {
  flex: 1;
  border-right: none;

  .el-menu-item {
    height: 50px;
    line-height: 50px;

    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }

    &.is-active {
      background-color: var(--sidebar-active);
      color: #fff;
    }
  }

  .el-submenu__title {
    height: 50px;
    line-height: 50px;

    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }

  .el-submenu .el-menu-item {
    background-color: rgba(0, 0, 0, 0.1);

    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}
</style>
