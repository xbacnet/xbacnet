/**
 * Vue Router Configuration
 * Defines all routes for the XBACnet Web Management Interface
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layout components
import Layout from '@/components/layout/Layout.vue'

// Views
import Dashboard from '@/views/Dashboard.vue'
import AnalogInputs from '@/views/objects/AnalogInputs.vue'
import AnalogOutputs from '@/views/objects/AnalogOutputs.vue'
import AnalogValues from '@/views/objects/AnalogValues.vue'
import BinaryInputs from '@/views/objects/BinaryInputs.vue'
import BinaryOutputs from '@/views/objects/BinaryOutputs.vue'
import BinaryValues from '@/views/objects/BinaryValues.vue'
import MultiStateInputs from '@/views/objects/MultiStateInputs.vue'
import MultiStateOutputs from '@/views/objects/MultiStateOutputs.vue'
import MultiStateValues from '@/views/objects/MultiStateValues.vue'
import UserManagement from '@/views/users/UserManagement.vue'
import Login from '@/views/auth/Login.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, hideLayout: true }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true, hideLayout: false },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
          title: 'Dashboard',
          icon: 'Dashboard'
        }
      },
      {
        path: 'analog-inputs',
        name: 'AnalogInputs',
        component: AnalogInputs,
        meta: {
          title: 'Analog Inputs',
          icon: 'TrendCharts'
        }
      },
      {
        path: 'analog-outputs',
        name: 'AnalogOutputs',
        component: AnalogOutputs,
        meta: {
          title: 'Analog Outputs',
          icon: 'Setting'
        }
      },
      {
        path: 'analog-values',
        name: 'AnalogValues',
        component: AnalogValues,
        meta: {
          title: 'Analog Values',
          icon: 'DataAnalysis'
        }
      },
      {
        path: 'binary-inputs',
        name: 'BinaryInputs',
        component: BinaryInputs,
        meta: {
          title: 'Binary Inputs',
          icon: 'Switch'
        }
      },
      {
        path: 'binary-outputs',
        name: 'BinaryOutputs',
        component: BinaryOutputs,
        meta: {
          title: 'Binary Outputs',
          icon: 'Operation'
        }
      },
      {
        path: 'binary-values',
        name: 'BinaryValues',
        component: BinaryValues,
        meta: {
          title: 'Binary Values',
          icon: 'Monitor'
        }
      },
      {
        path: 'multi-state-inputs',
        name: 'MultiStateInputs',
        component: MultiStateInputs,
        meta: {
          title: 'Multi-state Inputs',
          icon: 'Grid'
        }
      },
      {
        path: 'multi-state-outputs',
        name: 'MultiStateOutputs',
        component: MultiStateOutputs,
        meta: {
          title: 'Multi-state Outputs',
          icon: 'Menu'
        }
      },
      {
        path: 'multi-state-values',
        name: 'MultiStateValues',
        component: MultiStateValues,
        meta: {
          title: 'Multi-state Values',
          icon: 'List'
        }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: {
          title: 'User Management',
          icon: 'User'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
