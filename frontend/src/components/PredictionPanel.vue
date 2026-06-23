<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">价格预测</h3>
    
    <el-form :model="form" inline class="mb-4">
      <el-form-item label="供应商">
        <el-select v-model="form.supplierId" placeholder="选择供应商" @change="onSupplierChange">
          <el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="产品">
        <el-select v-model="form.productName" placeholder="选择产品">
          <el-option v-for="p in products" :key="p" :label="p" :value="p" />
        </el-select>
      </el-form-item>
      <el-form-item label="预测天数">
        <el-input-number v-model="form.daysAhead" :min="1" :max="30" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="predict" :loading="loading">
          <el-icon><TrendCharts /></el-icon> 预测
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="prediction" class="mt-4">
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
        <div class="flex items-center justify-between">
          <span class="text-gray-700">模型评估指标</span>
          <div class="flex gap-4">
            <span class="text-sm">MSE: {{ prediction.model_metrics.mse.toFixed(2) }}</span>
            <span class="text-sm font-semibold" :class="prediction.model_metrics.r2 > 0.5 ? 'text-green-600' : 'text-orange-600'">
              R²: {{ prediction.model_metrics.r2.toFixed(2) }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-3">
        <div v-for="(item, index) in prediction.predictions" :key="index" 
             class="bg-gray-50 rounded-lg p-3 text-center border-l-4"
             :class="index === 0 ? 'border-blue-500' : 'border-gray-300'">
          <div class="text-xs text-gray-500">{{ item.date }}</div>
          <div class="text-lg font-bold text-blue-600">{{ item.predicted_price }}</div>
          <div class="text-xs text-green-600">{{ item.confidence }}%</div>
        </div>
      </div>

      <div class="mt-6 h-60">
        <Line :data="predictionChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  DoughnutController
} from 'chart.js'
import { TrendCharts } from '@element-plus/icons-vue'
import type { Supplier, PriceHistory, PricePrediction } from '@/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  DoughnutController
)

const props = defineProps<{
  suppliers: Supplier[]
  priceHistory: PriceHistory[]
}>()

const emit = defineEmits<{
  predict: [supplierId: number, productName: string, daysAhead: number]
}>()

const form = reactive({
  supplierId: 0,
  productName: '',
  daysAhead: 7
})

const loading = ref(false)
const prediction = ref<PricePrediction | null>(null)

const products = computed(() => {
  return [...new Set(props.priceHistory.filter(p => p.supplier_id === form.supplierId).map(p => p.product_name))]
})

const onSupplierChange = () => {
  form.productName = ''
  prediction.value = null
}

const predict = async () => {
  if (!form.supplierId || !form.productName) {
    return
  }
  loading.value = true
  emit('predict', form.supplierId, form.productName, form.daysAhead)
  loading.value = false
}

watch(() => props.priceHistory, () => {
  if (form.supplierId) {
    const currentProducts = products.value
    if (currentProducts.length > 0 && !currentProducts.includes(form.productName)) {
      form.productName = currentProducts[0]
    }
  }
})

const predictionChartData = computed(() => {
  if (!prediction.value) return { labels: [], datasets: [] }
  
  const historyData = props.priceHistory
    .filter(p => p.supplier_id === prediction.value?.supplier_id && p.product_name === prediction.value?.product_name)
    .slice(-14)
  
  const labels = [
    ...historyData.map(h => h.date),
    ...prediction.value.predictions.map(p => p.date)
  ]
  
  const historyPrices = historyData.map(h => h.price)
  const predictedPrices = prediction.value.predictions.map(p => p.predicted_price)
  
  return {
    labels,
    datasets: [
      {
        label: '历史价格',
        data: [...historyPrices, ...Array(predictedPrices.length).fill(null)],
        borderColor: '#409EFF',
        backgroundColor: 'rgba(64, 158, 255, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 3
      },
      {
        label: '预测价格',
        data: [...Array(historyPrices.length).fill(null), ...predictedPrices],
        borderColor: '#67C23A',
        backgroundColor: 'rgba(103, 194, 58, 0.1)',
        borderDash: [5, 5],
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointStyle: 'star'
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false
    }
  },
  scales: {
    x: {
      ticks: {
        maxRotation: 45,
        minRotation: 45
      }
    },
    y: {
      beginAtZero: false
    }
  }
}
</script>