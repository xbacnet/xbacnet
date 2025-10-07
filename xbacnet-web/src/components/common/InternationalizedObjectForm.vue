<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="formRules"
    label-width="120px"
  >
    <el-form-item :label="$t('objects.objectIdentifier')" prop="object_identifier">
      <el-input 
        v-model="formData.object_identifier" 
        :disabled="isEdit"
        :placeholder="$t('objects.objectIdentifier')"
      />
    </el-form-item>
    
    <el-form-item :label="$t('objects.objectName')" prop="object_name">
      <el-input v-model="formData.object_name" :placeholder="$t('objects.objectName')" />
    </el-form-item>
    
    <el-form-item :label="$t('objects.presentValue')" prop="present_value">
      <el-input 
        v-model="formData.present_value" 
        type="number"
        :placeholder="$t('objects.presentValue')"
      />
    </el-form-item>
    
    <el-form-item :label="$t('objects.description')">
      <el-input 
        v-model="formData.description" 
        type="textarea" 
        :rows="3"
        :placeholder="$t('objects.description')"
      />
    </el-form-item>
    
    <el-form-item :label="$t('objects.eventState')" prop="event_state">
      <el-select v-model="formData.event_state" :placeholder="$t('objects.eventState')">
        <el-option :label="$t('states.normal')" value="normal" />
        <el-option :label="$t('states.fault')" value="fault" />
        <el-option :label="$t('states.offNormal')" value="offnormal" />
        <el-option :label="$t('states.highLimit')" value="highLimit" />
        <el-option :label="$t('states.lowLimit')" value="lowLimit" />
      </el-select>
    </el-form-item>
    
    <el-form-item :label="$t('objects.statusFlags')" prop="status_flags">
      <el-input v-model="formData.status_flags" :placeholder="$t('objects.statusFlags')" />
    </el-form-item>
    
    <el-form-item :label="$t('objects.units')" prop="units">
      <el-input v-model="formData.units" :placeholder="$t('objects.units')" />
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const formRef = ref()

const formData = reactive({
  object_identifier: '',
  object_name: '',
  present_value: '',
  description: '',
  event_state: 'normal',
  status_flags: '',
  units: '',
  ...props.modelValue
})

const formRules = {
  object_identifier: [
    { required: true, message: 'Object identifier is required', trigger: 'blur' }
  ],
  object_name: [
    { required: true, message: 'Object name is required', trigger: 'blur' }
  ],
  present_value: [
    { required: true, message: 'Present value is required', trigger: 'blur' }
  ]
}

// Watch for changes and emit to parent
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// Expose form methods
defineExpose({
  validate: () => formRef.value?.validate(),
  resetFields: () => formRef.value?.resetFields(),
  clearValidate: () => formRef.value?.clearValidate()
})
</script>

<style lang="scss" scoped>
.el-form-item {
  margin-bottom: 20px;
}

.el-input, .el-select {
  width: 100%;
}
</style>
