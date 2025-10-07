<template>
  <div class="status-indicator" :class="statusClass">
    <el-icon :size="iconSize">
      <component :is="statusIcon" />
    </el-icon>
    <span class="status-text">{{ statusText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  status: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'event' // 'event', 'service', 'connection'
  },
  iconSize: {
    type: Number,
    default: 16
  }
})

// Computed
const statusClass = computed(() => {
  const baseClass = 'status-indicator'
  const statusClass = `status-${props.status}`
  return `${baseClass} ${statusClass}`
})

const statusIcon = computed(() => {
  const iconMap = {
    // Event states
    normal: 'CircleCheck',
    fault: 'CircleClose',
    offnormal: 'Warning',
    highLimit: 'ArrowUp',
    lowLimit: 'ArrowDown',
    
    // Service states
    active: 'CircleCheck',
    inactive: 'CircleClose',
    maintenance: 'Tools',
    
    // Connection states
    connected: 'Connection',
    disconnected: 'Close',
    connecting: 'Loading'
  }
  
  return iconMap[props.status] || 'QuestionFilled'
})

const statusText = computed(() => {
  const textMap = {
    // Event states
    normal: 'Normal',
    fault: 'Fault',
    offnormal: 'Off Normal',
    highLimit: 'High Limit',
    lowLimit: 'Low Limit',
    
    // Service states
    active: 'Active',
    inactive: 'Inactive',
    maintenance: 'Maintenance',
    
    // Connection states
    connected: 'Connected',
    disconnected: 'Disconnected',
    connecting: 'Connecting'
  }
  
  return textMap[props.status] || props.status
})
</script>

<style lang="scss" scoped>
.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  
  .status-text {
    font-weight: 500;
  }
  
  // Event state colors
  &.status-normal {
    color: var(--success-color);
  }
  
  &.status-fault {
    color: var(--danger-color);
  }
  
  &.status-offnormal {
    color: var(--warning-color);
  }
  
  &.status-highLimit {
    color: var(--warning-color);
  }
  
  &.status-lowLimit {
    color: var(--warning-color);
  }
  
  // Service state colors
  &.status-active {
    color: var(--success-color);
  }
  
  &.status-inactive {
    color: var(--danger-color);
  }
  
  &.status-maintenance {
    color: var(--info-color);
  }
  
  // Connection state colors
  &.status-connected {
    color: var(--success-color);
  }
  
  &.status-disconnected {
    color: var(--danger-color);
  }
  
  &.status-connecting {
    color: var(--warning-color);
  }
}
</style>
