<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="140px"
    >
      <el-form-item label="Object Identifier" prop="object_identifier">
        <el-input-number
          v-model="formData.object_identifier"
          :min="1"
          :max="999999"
          style="width: 100%"
        />
      </el-form-item>
      
      <el-form-item label="Object Name" prop="object_name">
        <el-input v-model="formData.object_name" />
      </el-form-item>
      
      <el-form-item label="Present Value" prop="present_value">
        <el-input-number
          v-model="formData.present_value"
          :precision="3"
          style="width: 100%"
        />
      </el-form-item>
      
      <el-form-item label="Description">
        <el-input v-model="formData.description" type="textarea" />
      </el-form-item>
      
      <el-form-item label="Status Flags" prop="status_flags">
        <el-input v-model="formData.status_flags" maxlength="4" />
        <div class="form-help">
          Status flags (4 digits): In Alarm, Fault, Overridden, Out of Service
        </div>
      </el-form-item>
      
      <el-form-item label="Event State" prop="event_state">
        <el-select v-model="formData.event_state" style="width: 100%">
          <el-option label="Normal" value="normal" />
          <el-option label="Fault" value="fault" />
          <el-option label="Off Normal" value="offnormal" />
          <el-option label="High Limit" value="highLimit" />
          <el-option label="Low Limit" value="lowLimit" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="Out of Service" prop="out_of_service">
        <el-switch v-model="formData.out_of_service" />
      </el-form-item>
      
      <el-form-item label="Units" prop="units">
        <el-input v-model="formData.units" />
      </el-form-item>
      
      <el-form-item label="COV Increment">
        <el-input-number
          v-model="formData.cov_increment"
          :min="0"
          :precision="3"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="handleClose">Cancel</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">
        {{ isEdit ? 'Update' : 'Create' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  objectType: {
    type: String,
    default: 'object'
  },
  initialData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'submit'])

// Reactive data
const formRef = ref()
const submitting = ref(false)

// Form data
const formData = reactive({
  object_identifier: null,
  object_name: '',
  present_value: 0,
  description: '',
  status_flags: '0000',
  event_state: 'normal',
  out_of_service: false,
  units: '',
  cov_increment: 1.0
})

// Form validation rules
const formRules = {
  object_identifier: [
    { required: true, message: 'Please enter object identifier', trigger: 'blur' }
  ],
  object_name: [
    { required: true, message: 'Please enter object name', trigger: 'blur' }
  ],
  present_value: [
    { required: true, message: 'Please enter present value', trigger: 'blur' }
  ],
  status_flags: [
    { required: true, message: 'Please enter status flags', trigger: 'blur' },
    { pattern: /^[01]{4}$/, message: 'Status flags must be 4 digits (0 or 1)', trigger: 'blur' }
  ],
  event_state: [
    { required: true, message: 'Please select event state', trigger: 'change' }
  ],
  out_of_service: [
    { required: true, message: 'Please select out of service status', trigger: 'change' }
  ],
  units: [
    { required: true, message: 'Please enter units', trigger: 'blur' }
  ]
}

// Computed
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const dialogTitle = computed(() => {
  const action = props.isEdit ? 'Edit' : 'Create'
  const type = props.objectType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  return `${action} ${type}`
})

// Methods
function resetForm() {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  Object.assign(formData, {
    object_identifier: null,
    object_name: '',
    present_value: 0,
    description: '',
    status_flags: '0000',
    event_state: 'normal',
    out_of_service: false,
    units: '',
    cov_increment: 1.0
  })
}

function handleClose() {
  visible.value = false
  resetForm()
}

async function handleSubmit() {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitting.value = true
    
    const submitData = { ...formData }
    if (props.isEdit && props.initialData.id) {
      submitData.id = props.initialData.id
    }
    
    emit('submit', submitData)
  } catch (error) {
    console.error('Form validation error:', error)
    ElMessage.error('Please check the form data')
  } finally {
    submitting.value = false
  }
}

// Watch for initial data changes
watch(() => props.initialData, (newData) => {
  if (newData && Object.keys(newData).length > 0) {
    Object.assign(formData, newData)
  }
}, { deep: true, immediate: true })

// Watch for dialog visibility
watch(visible, (newVisible) => {
  if (newVisible && props.isEdit && props.initialData) {
    Object.assign(formData, props.initialData)
  } else if (!newVisible) {
    resetForm()
  }
})
</script>

<style lang="scss" scoped>
.form-help {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}
</style>
