<template>
  <div class="value-display" :class="displayClass">
    <div class="value-content">
      <span class="value-number" :style="{ color: valueColor }">
        {{ formattedValue }}
      </span>
      <span class="value-unit" v-if="unit">{{ unit }}</span>
    </div>
    <div class="value-label" v-if="label">{{ label }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  value: {
    type: [Number, String],
    required: true
  },
  unit: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  precision: {
    type: Number,
    default: 2
  },
  type: {
    type: String,
    default: 'number' // 'number', 'percentage', 'currency'
  },
  size: {
    type: String,
    default: 'medium' // 'small', 'medium', 'large'
  },
  color: {
    type: String,
    default: '' // Custom color
  },
  threshold: {
    type: Object,
    default: () => ({})
  }
})

// Computed
const formattedValue = computed(() => {
  const numValue = parseFloat(props.value)
  
  if (isNaN(numValue)) {
    return props.value
  }
  
  switch (props.type) {
    case 'percentage':
      return `${(numValue * 100).toFixed(props.precision)}%`
    case 'currency':
      return `$${numValue.toFixed(props.precision)}`
    default:
      return numValue.toFixed(props.precision)
  }
})

const displayClass = computed(() => {
  return `value-display--${props.size}`
})

const valueColor = computed(() => {
  if (props.color) {
    return props.color
  }
  
  if (props.threshold && Object.keys(props.threshold).length > 0) {
    const numValue = parseFloat(props.value)
    
    if (!isNaN(numValue)) {
      if (props.threshold.danger && numValue >= props.threshold.danger) {
        return 'var(--danger-color)'
      }
      if (props.threshold.warning && numValue >= props.threshold.warning) {
        return 'var(--warning-color)'
      }
      if (props.threshold.success && numValue >= props.threshold.success) {
        return 'var(--success-color)'
      }
    }
  }
  
  return 'var(--text-primary)'
})
</script>

<style lang="scss" scoped>
.value-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  
  .value-content {
    display: flex;
    align-items: baseline;
    gap: 4px;
    
    .value-number {
      font-weight: 600;
      line-height: 1;
    }
    
    .value-unit {
      font-size: 0.8em;
      color: var(--text-secondary);
      font-weight: 400;
    }
  }
  
  .value-label {
    font-size: 0.8em;
    color: var(--text-secondary);
    margin-top: 4px;
  }
  
  // Size variants
  &--small {
    .value-number {
      font-size: 18px;
    }
    
    .value-unit {
      font-size: 12px;
    }
    
    .value-label {
      font-size: 11px;
    }
  }
  
  &--medium {
    .value-number {
      font-size: 24px;
    }
    
    .value-unit {
      font-size: 14px;
    }
    
    .value-label {
      font-size: 12px;
    }
  }
  
  &--large {
    .value-number {
      font-size: 32px;
    }
    
    .value-unit {
      font-size: 16px;
    }
    
    .value-label {
      font-size: 14px;
    }
  }
}
</style>
