<template>
  <div class="dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <h1>XBACnet Dashboard</h1>
      <p>System overview and statistics</p>
    </div>
    
    <!-- Statistics Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in stats" :key="stat.key">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ color: stat.color }">
              <el-icon :size="32">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- Charts Row -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Object Distribution</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="objectDistributionChart" autoresize />
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>System Status</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="systemStatusChart" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- Recent Activity -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>Recent Activity</span>
              <el-button type="text" @click="refreshActivity">
                <el-icon><Refresh /></el-icon>
                Refresh
              </el-button>
            </div>
          </template>
          <el-table :data="recentActivity" style="width: 100%">
            <el-table-column prop="time" label="Time" width="180">
              <template #default="{ row }">
                {{ formatTime(row.time) }}
              </template>
            </el-table-column>
            <el-table-column prop="type" label="Type" width="120">
              <template #default="{ row }">
                <el-tag :type="getActivityTagType(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="user" label="User" width="120" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import { apiService } from '@/services/api'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

// Register ECharts components
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// Reactive data
const stats = ref([])
const recentActivity = ref([])
const systemStats = ref({})

// Computed charts
const objectDistributionChart = computed(() => {
  if (!systemStats.value.object_counts) return {}
  
  const data = Object.entries(systemStats.value.object_counts).map(([key, value]) => ({
    name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    value: value
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: 'Object Types',
        type: 'pie',
        radius: '50%',
        data: data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})

const systemStatusChart = computed(() => {
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['Active', 'Inactive', 'Fault', 'Maintenance']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: 'Objects',
        type: 'bar',
        data: [120, 30, 5, 10],
        itemStyle: {
          color: '#409eff'
        }
      }
    ]
  }
})

// Methods
async function loadStats() {
  try {
    const response = await apiService.getStats()
    systemStats.value = response
    
    // Update stats cards
    stats.value = [
      {
        key: 'total_objects',
        label: 'Total Objects',
        value: Object.values(response.object_counts || {}).reduce((a, b) => a + b, 0),
        icon: 'Grid',
        color: '#409eff'
      },
      {
        key: 'users',
        label: 'Users',
        value: response.object_counts?.user || 0,
        icon: 'User',
        color: '#67c23a'
      },
      {
        key: 'analog_objects',
        label: 'Analog Objects',
        value: (response.object_counts?.analog_input || 0) + 
               (response.object_counts?.analog_output || 0) + 
               (response.object_counts?.analog_value || 0),
        icon: 'TrendCharts',
        color: '#e6a23c'
      },
      {
        key: 'binary_objects',
        label: 'Binary Objects',
        value: (response.object_counts?.binary_input || 0) + 
               (response.object_counts?.binary_output || 0) + 
               (response.object_counts?.binary_value || 0),
        icon: 'Switch',
        color: '#f56c6c'
      }
    ]
  } catch (error) {
    console.error('Failed to load stats:', error)
    ElMessage.error('Failed to load statistics')
  }
}

function loadRecentActivity() {
  // Mock data for now - in real implementation, you would fetch from API
  recentActivity.value = [
    {
      time: new Date(),
      type: 'CREATE',
      description: 'Created new analog input object: Temperature_Sensor_1',
      user: 'admin'
    },
    {
      time: new Date(Date.now() - 300000),
      type: 'UPDATE',
      description: 'Updated binary output object: Light_Control_1',
      user: 'operator'
    },
    {
      time: new Date(Date.now() - 600000),
      type: 'LOGIN',
      description: 'User logged in',
      user: 'operator'
    },
    {
      time: new Date(Date.now() - 900000),
      type: 'DELETE',
      description: 'Deleted multi-state input object: HVAC_Mode_1',
      user: 'admin'
    }
  ]
}

function refreshActivity() {
  loadRecentActivity()
  ElMessage.success('Activity refreshed')
}

function formatTime(time) {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

function getActivityTagType(type) {
  const typeMap = {
    'CREATE': 'success',
    'UPDATE': 'warning',
    'DELETE': 'danger',
    'LOGIN': 'info',
    'LOGOUT': 'info'
  }
  return typeMap[type] || 'info'
}

// Lifecycle
onMounted(() => {
  loadStats()
  loadRecentActivity()
  
  // Refresh stats every 30 seconds
  setInterval(loadStats, 30000)
})
</script>

<style lang="scss" scoped>
.dashboard {
  .page-header {
    margin-bottom: 20px;
    
    h1 {
      color: var(--text-primary);
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 5px;
    }
    
    p {
      color: var(--text-secondary);
      font-size: 14px;
    }
  }
  
  .stats-row {
    margin-bottom: 20px;
  }
  
  .stat-card {
    height: 100px;
    
    .stat-content {
      display: flex;
      align-items: center;
      height: 100%;
      
      .stat-icon {
        margin-right: 15px;
      }
      
      .stat-info {
        flex: 1;
        
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--text-primary);
          line-height: 1;
        }
        
        .stat-label {
          font-size: 14px;
          color: var(--text-secondary);
          margin-top: 5px;
        }
      }
    }
  }
  
  .charts-row {
    margin-bottom: 20px;
  }
  
  .chart-card,
  .activity-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      color: var(--text-primary);
    }
    
    .chart-container {
      height: 300px;
    }
  }
}
</style>
