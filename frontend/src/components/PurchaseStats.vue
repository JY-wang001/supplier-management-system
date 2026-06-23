<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">采购统计</h3>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-blue-50 rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-blue-600">{{ totalPurchases }}</div>
        <div class="text-sm text-gray-600">采购次数</div>
      </div>
      <div class="bg-green-50 rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-green-600">{{ totalQuantity }}</div>
        <div class="text-sm text-gray-600">采购总量</div>
      </div>
      <div class="bg-yellow-50 rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-yellow-600">{{ avgPrice }}</div>
        <div class="text-sm text-gray-600">平均单价</div>
      </div>
      <div class="bg-purple-50 rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-purple-600">{{ totalAmount }}</div>
        <div class="text-sm text-gray-600">总金额</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PurchaseRecord } from '@/api'

const props = defineProps<{
  purchaseRecords: PurchaseRecord[]
}>()

const totalPurchases = computed(() => props.purchaseRecords.length)

const totalQuantity = computed(() => {
  return props.purchaseRecords.reduce((sum, item) => sum + item.quantity, 0).toFixed(2)
})

const avgPrice = computed(() => {
  if (props.purchaseRecords.length === 0) return '0.00'
  const total = props.purchaseRecords.reduce((sum, item) => sum + item.unit_price, 0)
  return (total / props.purchaseRecords.length).toFixed(2)
})

const totalAmount = computed(() => {
  return props.purchaseRecords.reduce((sum, item) => sum + (item.total_amount || 0), 0).toFixed(2)
})
</script>