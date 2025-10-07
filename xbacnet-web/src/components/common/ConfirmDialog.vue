<template>
  <el-dialog
    v-model="visible"
    :title="title"
    width="400px"
    :show-close="false"
  >
    <div class="confirm-content">
      <el-icon class="confirm-icon" :class="iconClass" :size="48">
        <component :is="iconComponent" />
      </el-icon>
      <div class="confirm-message">
        <p class="message-text">{{ message }}</p>
        <p class="message-detail" v-if="detail">{{ detail }}</p>
      </div>
    </div>
    
    <template #footer>
      <div class="confirm-actions">
        <el-button @click="handleCancel" :disabled="loading">
          {{ cancelText }}
        </el-button>
        <el-button 
          :type="confirmType" 
          @click="handleConfirm" 
          :loading="loading"
        >
          {{ confirmText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm'
  },
  message: {
    type: String,
    required: true
  },
  detail: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'warning', // 'info', 'success', 'warning', 'danger'
    validator: (value) => ['info', 'success', 'warning', 'danger'].includes(value)
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

// Computed
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const iconComponent = computed(() => {
  const iconMap = {
    info: 'InfoFilled',
    success: 'CircleCheck',
    warning: 'Warning',
    danger: 'CircleClose'
  }
  return iconMap[props.type] || 'QuestionFilled'
})

const iconClass = computed(() => {
  return `confirm-icon--${props.type}`
})

const confirmType = computed(() => {
  const typeMap = {
    info: 'primary',
    success: 'success',
    warning: 'warning',
    danger: 'danger'
  }
  return typeMap[props.type] || 'primary'
})

// Methods
function handleConfirm() {
  emit('confirm')
}

function handleCancel() {
  emit('cancel')
  visible.value = false
}
</script>

<style lang="scss" scoped>
.confirm-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 0;
  
  .confirm-icon {
    flex-shrink: 0;
    
    &--info {
      color: var(--info-color);
    }
    
    &--success {
      color: var(--success-color);
    }
    
    &--warning {
      color: var(--warning-color);
    }
    
    &--danger {
      color: var(--danger-color);
    }
  }
  
  .confirm-message {
    flex: 1;
    
    .message-text {
      font-size: 16px;
      font-weight: 500;
      color: var(--text-primary);
      margin: 0 0 8px 0;
      line-height: 1.5;
    }
    
    .message-detail {
      font-size: 14px;
      color: var(--text-secondary);
      margin: 0;
      line-height: 1.4;
    }
  }
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
