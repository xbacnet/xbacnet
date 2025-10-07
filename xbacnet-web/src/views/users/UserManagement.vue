<template>
  <div class="user-management">
    <!-- Page Header -->
    <div class="page-header">
      <h1>User Management</h1>
      <p>Manage system users and permissions</p>
    </div>
    
    <!-- Action Buttons -->
    <div class="action-buttons">
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        Create User
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
        <el-table-column prop="name" :label="$t('users.username')" width="150" />
        <el-table-column prop="display_name" :label="$t('users.displayName')" width="150" />
        <el-table-column prop="email" :label="$t('users.email')" min-width="200" />
        <el-table-column prop="is_admin" :label="$t('users.admin')" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_admin ? 'danger' : 'success'">
              {{ row.is_admin ? 'Yes' : 'No' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="uuid" label="UUID" min-width="250" show-overflow-tooltip />
        <el-table-column :label="$t('common.actions')" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editUser(row)">
              <el-icon><Edit /></el-icon>
              Edit
            </el-button>
            <el-button size="small" type="danger" @click="deleteUser(row)">
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
        label-width="120px"
      >
        <el-form-item :label="$t('users.username')" prop="name">
          <el-input 
            v-model="formData.name" 
            :disabled="isEdit"
            placeholder="Enter username"
          />
        </el-form-item>
        
        <el-form-item :label="$t('users.displayName')" prop="display_name">
          <el-input v-model="formData.display_name" placeholder="Enter display name" />
        </el-form-item>
        
        <el-form-item :label="$t('users.email')" prop="email">
          <el-input v-model="formData.email" type="email" placeholder="Enter email address" />
        </el-form-item>
        
        <el-form-item :label="$t('users.password')" prop="password" v-if="!isEdit">
          <el-input 
            v-model="formData.password" 
            type="password" 
            placeholder="Enter password"
            show-password
          />
        </el-form-item>
        
        <el-form-item :label="$t('users.newPassword')" prop="new_password" v-if="isEdit">
          <el-input 
            v-model="formData.new_password" 
            type="password" 
            placeholder="Leave empty to keep current password"
            show-password
          />
        </el-form-item>
        
        <el-form-item :label="$t('users.admin')" prop="is_admin">
          <el-switch v-model="formData.is_admin" />
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
  name: '',
  display_name: '',
  email: '',
  password: '',
  new_password: '',
  is_admin: false
})

// Form validation rules
const formRules = {
  name: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 128, message: 'Username must be between 3 and 128 characters', trigger: 'blur' }
  ],
  display_name: [
    { required: true, message: 'Please enter display name', trigger: 'blur' },
    { min: 1, max: 128, message: 'Display name must be between 1 and 128 characters', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Please enter email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, max: 128, message: 'Password must be between 6 and 128 characters', trigger: 'blur' }
  ]
}

// Computed
const dialogTitle = computed(() => {
  return isEdit.value ? 'Edit User' : 'Create User'
})

// Methods
async function loadData() {
  loading.value = true
  try {
    const response = await apiService.getUsers({
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    tableData.value = response.data
    total.value = response.pagination.total
  } catch (error) {
    console.error('Failed to load users:', error)
    ElMessage.error('Failed to load users')
  } finally {
    loading.value = false
  }
}

function showCreateDialog() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function editUser(row) {
  isEdit.value = true
  Object.assign(formData, {
    name: row.name,
    display_name: row.display_name,
    email: row.email,
    is_admin: row.is_admin,
    password: '',
    new_password: ''
  })
  dialogVisible.value = true
}

async function deleteUser(row) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete user "${row.display_name}"?`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    await apiService.deleteUser(row.id)
    ElMessage.success('User deleted successfully')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete user:', error)
      ElMessage.error('Failed to delete user')
    }
  }
}

async function submitForm() {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitting.value = true
    
    const submitData = { ...formData }
    
    if (isEdit.value) {
      // Remove password fields if not changing password
      if (!submitData.new_password) {
        delete submitData.password
        delete submitData.new_password
      } else {
        submitData.password = submitData.new_password
        delete submitData.new_password
      }
      
      await apiService.updateUser(formData.id, submitData)
      ElMessage.success('User updated successfully')
    } else {
      await apiService.createUser(submitData)
      ElMessage.success('User created successfully')
    }
    
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('Failed to save user:', error)
    ElMessage.error('Failed to save user')
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  Object.assign(formData, {
    name: '',
    display_name: '',
    email: '',
    password: '',
    new_password: '',
    is_admin: false
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

// Lifecycle
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.user-management {
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
    .pagination {
      margin-top: 20px;
      display: flex;
      justify-content: center;
    }
  }
}
</style>
