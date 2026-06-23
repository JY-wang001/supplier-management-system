<template>
  <el-dialog :title="supplier ? '编辑供应商' : '添加供应商'" :visible.sync="visible" width="600px">
    <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
      <el-form-item label="供应商名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入供应商名称" />
      </el-form-item>
      <el-form-item label="联系人" prop="contact_person">
        <el-input v-model="form.contact_person" placeholder="请输入联系人" />
      </el-form-item>
      <el-form-item label="电话" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入联系电话" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱地址" />
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="form.address" type="textarea" :rows="3" placeholder="请输入地址" />
      </el-form-item>
      <el-form-item label="产品类型" prop="product_type">
        <el-select v-model="form.product_type" placeholder="请选择产品类型">
          <el-option label="食品原料" value="食品原料" />
          <el-option label="化工原料" value="化工原料" />
          <el-option label="农产品" value="农产品" />
          <el-option label="机械设备" value="机械设备" />
          <el-option label="其他" value="其他" />
        </el-select>
      </el-form-item>
      <el-form-item label="信用评级" prop="credit_rating">
        <el-rate v-model="form.credit_rating" :max="5" show-score text-color="#ff9900" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, reactive, type ComponentPublicInstance } from 'vue'
import type { Supplier } from '@/api'

const props = defineProps<{
  visible: boolean
  supplier?: Supplier | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  submit: [data: Omit<Supplier, 'id' | 'created_at' | 'updated_at'>]
}>()

const formRef = ref<ComponentPublicInstance | null>(null)

const form = reactive({
  name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  product_type: '',
  credit_rating: 0
})

const rules = {
  name: [{ required: true, message: '请输入供应商名称', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

watch(() => props.supplier, (newSupplier) => {
  if (newSupplier) {
    Object.assign(form, newSupplier)
  } else {
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
    form.credit_rating = 0
  }
}, { immediate: true })

const submit = async () => {
  if (!formRef.value) return
  
  try {
    await (formRef.value as any).validate()
    emit('submit', { ...form })
    emit('update:visible', false)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>