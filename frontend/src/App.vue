<template>
  <div class="min-h-screen bg-gray-100">
    <LoginForm v-if="!isLoggedIn" @login="handleLogin" />
    
    <template v-else>
      <header class="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
        <div class="container mx-auto px-4 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <el-icon class="text-2xl"><OfficeBuilding /></el-icon>
              <h1 class="text-xl md:text-2xl font-bold">供应商管理与价格预测系统</h1>
            </div>
            <div class="hidden md:flex items-center gap-4">
              <el-button text @click="activeTab = 'suppliers'">供应商管理</el-button>
              <el-button text @click="activeTab = 'analytics'">数据分析</el-button>
              <el-button text @click="activeTab = 'prediction'">价格预测</el-button>
              <el-button text @click="logout">退出登录</el-button>
            </div>
            <div class="flex items-center gap-2 md:hidden">
              <span class="text-sm">{{ currentUser?.username }}</span>
              <el-button @click="mobileMenuVisible = !mobileMenuVisible">
                <el-icon><Menu /></el-icon>
              </el-button>
            </div>
          </div>

          <div v-if="mobileMenuVisible" class="mt-4 flex flex-col gap-2">
            <el-button text @click="activeTab = 'suppliers'; mobileMenuVisible = false">供应商管理</el-button>
            <el-button text @click="activeTab = 'analytics'; mobileMenuVisible = false">数据分析</el-button>
            <el-button text @click="activeTab = 'prediction'; mobileMenuVisible = false">价格预测</el-button>
            <el-button text @click="logout; mobileMenuVisible = false">退出登录</el-button>
          </div>
        </div>
      </header>

    <main class="container mx-auto px-4 py-6">
      <div v-if="activeTab === 'suppliers'" class="space-y-6">
        <SupplierTable
          :suppliers="suppliers"
          :total="suppliers.length"
          :page="currentPage"
          :page-size="pageSize"
          @add="showAddForm"
          @view="viewSupplier"
          @edit="showEditForm"
          @delete="deleteSupplier"
        />

        <div v-if="selectedSupplier" class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">供应商详情</h2>
            <el-button @click="selectedSupplier = null">关闭</el-button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div class="bg-blue-50 rounded-lg p-4">
              <div class="text-sm text-gray-600">供应商名称</div>
              <div class="text-lg font-bold text-blue-600">{{ selectedSupplier.name }}</div>
            </div>
            <div class="bg-green-50 rounded-lg p-4">
              <div class="text-sm text-gray-600">产品类型</div>
              <div class="text-lg font-bold text-green-600">{{ selectedSupplier.product_type }}</div>
            </div>
            <div class="bg-yellow-50 rounded-lg p-4">
              <div class="text-sm text-gray-600">联系人</div>
              <div class="text-lg font-bold text-yellow-600">{{ selectedSupplier.contact_person }}</div>
            </div>
            <div class="bg-purple-50 rounded-lg p-4">
              <div class="text-sm text-gray-600">信用评级</div>
              <el-rate :value="selectedSupplier.credit_rating" disabled :max="5" show-score text-color="#ff9900" />
            </div>
          </div>

          <div class="mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">联系方式</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="flex items-center gap-2">
                <el-icon class="text-blue-500"><Phone /></el-icon>
                <span>{{ selectedSupplier.phone }}</span>
              </div>
              <div class="flex items-center gap-2">
                <el-icon class="text-green-500"><Message /></el-icon>
                <span>{{ selectedSupplier.email }}</span>
              </div>
              <div class="flex items-center gap-2">
                <el-icon class="text-orange-500"><Location /></el-icon>
                <span>{{ selectedSupplier.address }}</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-4">价格历史</h3>
              <el-table :data="selectedSupplierPriceHistory" border style="width: 100%">
                <el-table-column prop="product_name" label="产品" />
                <el-table-column prop="price" label="价格" />
                <el-table-column prop="date" label="日期" />
              </el-table>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-4">采购记录</h3>
              <el-table :data="selectedSupplierPurchaseRecords" border style="width: 100%">
                <el-table-column prop="product_name" label="产品" />
                <el-table-column prop="quantity" label="数量" />
                <el-table-column prop="unit_price" label="单价" />
                <el-table-column prop="purchase_date" label="日期" />
              </el-table>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'analytics'" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <PriceChart title="价格趋势" :price-history="allPriceHistory" />
        </div>
        <PurchaseStats :purchase-records="allPurchaseRecords" />
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">供应商对比</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="supplier in suppliers" :key="supplier.id" class="bg-gray-50 rounded-lg p-4">
              <div class="font-semibold text-gray-800">{{ supplier.name }}</div>
              <div class="text-sm text-gray-600">产品类型: {{ supplier.product_type }}</div>
              <div class="text-sm text-gray-600">信用评级: {{ supplier.credit_rating }}</div>
              <div class="text-sm text-blue-600">采购次数: {{ getPurchaseCount(supplier.id) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'prediction'" class="space-y-6">
        <PredictionPanel
          :suppliers="suppliers"
          :price-history="allPriceHistory"
          @predict="handlePredict"
        />
      </div>
    </main>

    <SupplierForm
      :visible="showForm"
      :supplier="editingSupplier"
      @update:visible="showForm = false"
      @submit="handleSupplierSubmit"
    />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { OfficeBuilding, Menu, Phone, Message, Location } from '@element-plus/icons-vue'
import SupplierTable from '@/components/SupplierTable.vue'
import SupplierForm from '@/components/SupplierForm.vue'
import PriceChart from '@/components/PriceChart.vue'
import PurchaseStats from '@/components/PurchaseStats.vue'
import PredictionPanel from '@/components/PredictionPanel.vue'
import LoginForm from '@/components/LoginForm.vue'
import { supplierApi, predictionApi, type Supplier, type PriceHistory, type PurchaseRecord, type User } from '@/api'
import { ElMessage } from 'element-plus'

const activeTab = ref('suppliers')
const mobileMenuVisible = ref(false)
const suppliers = ref<Supplier[]>([])
const allPriceHistory = ref<PriceHistory[]>([])
const allPurchaseRecords = ref<PurchaseRecord[]>([])
const showForm = ref(false)
const editingSupplier = ref<Supplier | null>(null)
const selectedSupplier = ref<Supplier | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)
const isLoggedIn = ref(false)
const currentUser = ref<User | null>(null)

const selectedSupplierPriceHistory = computed(() => {
  if (!selectedSupplier.value) return []
  return allPriceHistory.value.filter(p => p.supplier_id === selectedSupplier.value?.id)
})

const selectedSupplierPurchaseRecords = computed(() => {
  if (!selectedSupplier.value) return []
  return allPurchaseRecords.value.filter(p => p.supplier_id === selectedSupplier.value?.id)
})

const getPurchaseCount = (supplierId: number) => {
  return allPurchaseRecords.value.filter(p => p.supplier_id === supplierId).length
}

const loadSuppliers = async () => {
  try {
    const response = await supplierApi.getAll()
    suppliers.value = response.data
  } catch (error) {
    ElMessage.error('加载供应商失败')
  }
}

const loadPriceHistory = async () => {
  try {
    for (const supplier of suppliers.value) {
      const response = await supplierApi.getPriceHistory(supplier.id)
      allPriceHistory.value = [...allPriceHistory.value, ...response.data]
    }
  } catch (error) {
    console.error('加载价格历史失败')
  }
}

const loadPurchaseRecords = async () => {
  try {
    for (const supplier of suppliers.value) {
      const response = await supplierApi.getPurchaseRecords(supplier.id)
      allPurchaseRecords.value = [...allPurchaseRecords.value, ...response.data]
    }
  } catch (error) {
    console.error('加载采购记录失败')
  }
}

const showAddForm = () => {
  editingSupplier.value = null
  showForm.value = true
}

const showEditForm = (supplier: Supplier) => {
  editingSupplier.value = supplier
  showForm.value = true
}

const viewSupplier = (supplier: Supplier) => {
  selectedSupplier.value = supplier
}

const deleteSupplier = async (supplier: Supplier) => {
  try {
    await supplierApi.delete(supplier.id)
    suppliers.value = suppliers.value.filter(s => s.id !== supplier.id)
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleSupplierSubmit = async (data: Omit<Supplier, 'id' | 'created_at' | 'updated_at'>) => {
  try {
    if (editingSupplier.value) {
      await supplierApi.update(editingSupplier.value.id, data)
      ElMessage.success('更新成功')
    } else {
      await supplierApi.create(data)
      ElMessage.success('创建成功')
    }
    await loadSuppliers()
    await loadPriceHistory()
    await loadPurchaseRecords()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handlePredict = async (supplierId: number, productName: string, daysAhead: number) => {
  try {
    const response = await predictionApi.predictPrice(supplierId, productName, daysAhead)
    console.log('预测结果:', response.data)
    ElMessage.success('预测完成')
  } catch (error) {
    ElMessage.error('预测失败')
  }
}

const handleLogin = async (token: string) => {
  isLoggedIn.value = true
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }
  await loadSuppliers()
  await loadPriceHistory()
  await loadPurchaseRecords()
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  currentUser.value = null
  suppliers.value = []
  allPriceHistory.value = []
  allPurchaseRecords.value = []
  ElMessage.success('已退出登录')
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    isLoggedIn.value = true
    const userStr = localStorage.getItem('user')
    if (userStr) {
      currentUser.value = JSON.parse(userStr)
    }
    await loadSuppliers()
    await loadPriceHistory()
    await loadPurchaseRecords()
  }
})
</script>