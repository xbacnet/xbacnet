<template>
  <div class="analog-inputs">
    <!-- Page Header -->
    <div class="page-header">
      <h1>Binary Value Objects</h1>
      <p>Manage binary value objects in the BACnet system</p>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        Create Binary Value
      </el-button>
      <el-button @click="loadData">
        <el-icon><Refresh /></el-icon>
        Refresh
      </el-button>
    </div>

    <!-- Data Table -->
    <el-card class="data-table">
      <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="object_identifier" label="Object ID" width="120" />
        <el-table-column prop="object_name" label="Object Name" min-width="150" />
        <el-table-column prop="present_value" label="Present Value" width="120">
          <template #default="{ row }">
            <span class="value-display">{{ row.present_value }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="Description" min-width="200" />
        <el-table-column prop="units" label="Units" width="120" />
        <el-table-column prop="event_state" label="Event State" width="120">
          <template #default="{ row }">
            <el-tag :type="getEventStateType(row.event_state)">
              {{ row.event_state }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="out_of_service" label="Out of Service" width="120">
          <template #default="{ row }">
            <el-tag :type="row.out_of_service ? 'danger' : 'success'">
              {{ row.out_of_service ? 'Yes' : 'No' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editObject(row)">
              <el-icon><Edit /></el-icon>
              Edit
            </el-button>
            <el-button size="small" type="danger" @click="deleteObject(row)">
              <el-icon><Delete /></el-icon>
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Create/Edit Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
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
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">
          {{ isEdit ? 'Update' : 'Create' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { apiService } from '@/services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

// Reactive data
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const tableData = ref([])
const formRef = ref()

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
const dialogTitle = computed(() => {
  return isEdit.value ? 'Edit Binary Value' : 'Create Binary Value'
})

// Methods
async function loadData() {
  loading.value = true
  try {
    const response = await apiService.getAnalogInputs({
      page: currentPage.value,
      page_size: pageSize.value
    })

    tableData.value = response.data
    total.value = response.pagination.total
  } catch (error) {
    console.error('Failed to load analog inputs:', error)
    ElMessage.error('Failed to load analog inputs')
  } finally {
    loading.value = false
  }
}

function showCreateDialog() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function editObject(row) {
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

async function deleteObject(row) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete analog input "${row.object_name}"?`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    await apiService.deleteAnalogInput(row.id)
    ElMessage.success('Analog input deleted successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete analog input:', error)
      ElMessage.error('Failed to delete analog input')
    }
  }
}

async function submitForm() {
  if (!formRef.value) return

  try {
    const valid = await formRef.value.validate()
    if (!valid) return

    submitting.value = true

    if (isEdit.value) {
      await apiService.updateAnalogInput(formData.id, formData)
      ElMessage.success('Analog input updated successfully')
    } else {
      await apiService.createAnalogInput(formData)
      ElMessage.success('Analog input created successfully')
    }

    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Failed to save analog input:', error)
    ElMessage.error('Failed to save analog input')
  } finally {
    submitting.value = false
  }
}

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

function handleSizeChange(newSize) {
  pageSize.value = newSize
  currentPage.value = 1
  loadData()
}

function handleCurrentChange(newPage) {
  currentPage.value = newPage
  loadData()
}

function getEventStateType(state) {
  const typeMap = {
    'normal': 'success',
    'fault': 'danger',
    'offnormal': 'warning',
    'highLimit': 'warning',
    'lowLimit': 'warning'
  }
  return typeMap[state] || 'info'
}

// Lifecycle
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.analog-inputs {
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

  .action-buttons {
    margin-bottom: 20px;
  }

  .data-table {
    .value-display {
      font-weight: 500;
      color: var(--primary-color);
    }

    .pagination {
      margin-top: 20px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
