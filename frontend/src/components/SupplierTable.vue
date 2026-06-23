<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-gray-800">供应商列表</h2>
      <el-button type="primary" @click="$emit('add')">
        <el-icon><Plus /></el-icon> 添加供应商
      </el-button>
    </div>

    <el-table :data="suppliers" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="供应商名称" min-width="150" />
      <el-table-column prop="contact_person" label="联系人" width="100" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="product_type" label="产品类型" width="120" />
      <el-table-column prop="credit_rating" label="信用评级" width="100">
        <template #default="{ row }">
          <el-rate :value="row.credit_rating" disabled :max="5" show-score text-color="#ff9900" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="$emit('view', row)">查看详情</el-button>
          <el-button size="small" type="primary" @click="$emit('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="$emit('delete', row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      class="mt-4 flex justify-center"
      :current-page="page"
      :page-size="pageSize"
      :total="total"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import type { Supplier } from '@/api'

defineProps<{
  suppliers: Supplier[]
  total: number
  page: number
  pageSize: number
}>()

const emit = defineEmits<{
  add: []
  view: [supplier: Supplier]
  edit: [supplier: Supplier]
  delete: [supplier: Supplier]
}>()

const handlePageChange = (page: number) => {
  emit('page-change', page)
}
</script>