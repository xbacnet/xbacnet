<template>
  <div class="data-table">
    <!-- Table Actions -->
    <div class="table-actions" v-if="showActions">
      <el-button type="primary" @click="$emit('create')" v-if="showCreate">
        <el-icon><Plus /></el-icon>
        {{ createText }}
      </el-button>
      <el-button @click="$emit('refresh')" v-if="showRefresh">
        <el-icon><Refresh /></el-icon>
        {{ refreshText }}
      </el-button>
      <el-button @click="exportData" v-if="showExport">
        <el-icon><Download /></el-icon>
        Export
      </el-button>
    </div>
    
    <!-- Data Table -->
    <el-card>
      <el-table
        :data="data"
        v-loading="loading"
        stripe
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
      >
        <!-- Selection column -->
        <el-table-column
          type="selection"
          width="55"
          v-if="showSelection"
        />
        
        <!-- Dynamic columns -->
        <el-table-column
          v-for="column in columns"
          :key="column.prop"
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          :fixed="column.fixed"
          :sortable="column.sortable"
          :show-overflow-tooltip="column.showOverflowTooltip"
        >
          <template #default="{ row, $index }" v-if="column.slot">
            <slot :name="column.slot" :row="row" :index="$index" />
          </template>
        </el-table-column>
        
        <!-- Actions column -->
        <el-table-column
          label="Actions"
          :width="actionsWidth"
          fixed="right"
          v-if="showActionsColumn"
        >
          <template #default="{ row, $index }">
            <slot name="actions" :row="row" :index="$index">
              <el-button size="small" @click="$emit('edit', row)">
                <el-icon><Edit /></el-icon>
                Edit
              </el-button>
              <el-button size="small" type="danger" @click="$emit('delete', row)">
                <el-icon><Delete /></el-icon>
                Delete
              </el-button>
            </slot>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- Pagination -->
      <div class="pagination" v-if="showPagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="pageSizes"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { exportAsCSV, exportAsJSON } from '@/utils'

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  columns: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  total: {
    type: Number,
    default: 0
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 20
  },
  pageSizes: {
    type: Array,
    default: () => [10, 20, 50, 100]
  },
  showPagination: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showActionsColumn: {
    type: Boolean,
    default: true
  },
  showSelection: {
    type: Boolean,
    default: false
  },
  showCreate: {
    type: Boolean,
    default: true
  },
  showRefresh: {
    type: Boolean,
    default: true
  },
  showExport: {
    type: Boolean,
    default: true
  },
  createText: {
    type: String,
    default: 'Create'
  },
  refreshText: {
    type: String,
    default: 'Refresh'
  },
  actionsWidth: {
    type: Number,
    default: 200
  },
  exportFilename: {
    type: String,
    default: 'data'
  }
})

// Emits
const emit = defineEmits([
  'create',
  'edit',
  'delete',
  'refresh',
  'size-change',
  'current-change',
  'selection-change',
  'sort-change'
])

// Methods
function handleSizeChange(newSize) {
  emit('size-change', newSize)
}

function handleCurrentChange(newPage) {
  emit('current-change', newPage)
}

function handleSelectionChange(selection) {
  emit('selection-change', selection)
}

function handleSortChange(sortInfo) {
  emit('sort-change', sortInfo)
}

function exportData() {
  if (props.data.length === 0) {
    return
  }
  
  const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
  const filename = `${props.exportFilename}_${timestamp}`
  
  exportAsCSV(props.data, `${filename}.csv`)
}
</script>

<style lang="scss" scoped>
.data-table {
  .table-actions {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>
