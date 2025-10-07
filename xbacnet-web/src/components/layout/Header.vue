<template>
  <div class="header-container">
    <!-- Left side -->
    <div class="header-left">
      <el-button
        type="text"
        @click="toggleSidebar"
        class="sidebar-toggle"
      >
        <el-icon><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
      </el-button>

      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item v-if="currentRoute.meta?.title">
          {{ currentRoute.meta.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- Right side -->
    <div class="header-right">
      <!-- Theme toggle -->
      <el-button
        type="text"
        @click="toggleTheme"
        class="theme-toggle"
      >
        <el-icon><Sunny v-if="currentTheme === 'dark'" /><Moon v-else /></el-icon>
      </el-button>

      <!-- User menu -->
      <el-dropdown @command="handleCommand" class="user-dropdown">
        <div class="user-info">
          <el-avatar :size="32" :src="userAvatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <span class="username">{{ currentUser?.display_name || 'User' }}</span>
          <el-icon class="arrow-down"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              Profile
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              Settings
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              Logout
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()

const isCollapsed = computed(() => appStore.sidebarCollapsed)
const currentTheme = computed(() => appStore.currentTheme)
const currentUser = computed(() => authStore.currentUser)
const currentRoute = computed(() => route)

const userAvatar = computed(() => {
  // You can add avatar URL logic here
  return null
})

function toggleSidebar() {
  appStore.toggleSidebar()
}

function toggleTheme() {
  const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
  appStore.setTheme(newTheme)
}

async function handleCommand(command) {
  switch (command) {
    case 'profile':
      // Navigate to profile page
      ElMessage.info('Profile page coming soon')
      break
    case 'settings':
      // Navigate to settings page
      ElMessage.info('Settings page coming soon')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm(
          'Are you sure you want to logout?',
          'Confirm Logout',
          {
            confirmButtonText: 'Logout',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }
        )

        await authStore.logout()
        ElMessage.success('Logged out successfully')
        router.push('/login')
      } catch (error) {
        // User cancelled
      }
      break
  }
}
</script>

<style lang="scss" scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.sidebar-toggle {
  color: var(--text-primary);
  font-size: 18px;

  &:hover {
    color: var(--primary-color);
  }
}

.breadcrumb {
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      color: var(--text-secondary);
      font-weight: normal;

      &.is-link {
        color: var(--primary-color);

        &:hover {
          color: var(--primary-color);
        }
      }
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.theme-toggle {
  color: var(--text-primary);
  font-size: 18px;

  &:hover {
    color: var(--primary-color);
  }
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 10px;
  border-radius: 6px;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--main-bg);
  }

  .username {
    color: var(--text-primary);
    font-size: 14px;
  }

  .arrow-down {
    color: var(--text-secondary);
    font-size: 12px;
  }
}

// Responsive design
@media (max-width: 768px) {
  .header-container {
    padding: 0 10px;
  }

  .breadcrumb {
    display: none;
  }

  .username {
    display: none;
  }
}
</style>
