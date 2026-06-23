<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md transform transition-all duration-300 hover:scale-[1.02]">
      <div class="text-center mb-8">
        <div class="bg-gradient-to-r from-blue-500 to-purple-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
          <el-icon class="text-4xl text-white"><Lock /></el-icon>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">供应商管理系统</h1>
        <p class="text-gray-500 mt-2">智能采购与价格预测平台</p>
      </div>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px" class="space-y-5">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
            prefix-icon="User"
            class="rounded-lg"
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="Lock"
            class="rounded-lg"
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            @click="submit" 
            class="w-full rounded-lg font-medium"
            size="large"
            :loading="loading"
          >
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="text-center mt-6">
        <el-button text @click="showRegister = true" class="text-blue-600 hover:text-blue-700">
          注册新账户
        </el-button>
      </div>

      <div v-if="error" class="mt-4">
        <el-alert type="error" :title="error" show-icon class="rounded-lg" />
      </div>
    </div>

    <el-dialog 
      v-model="showRegister" 
      title="注册新账户" 
      width="450px" 
      class="register-dialog"
    >
      <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef" label-width="80px" class="space-y-5">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="registerForm.username" 
            placeholder="请输入用户名" 
            size="large"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="registerForm.email" 
            placeholder="请输入邮箱" 
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码" 
            size="large"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码" 
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegister = false" size="large">取消</el-button>
        <el-button type="primary" @click="register" :loading="registerLoading" size="large">注册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, type ComponentPublicInstance } from 'vue'
import { Lock } from '@element-plus/icons-vue'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'

const emit = defineEmits<{
  login: [token: string]
}>()

const formRef = ref<ComponentPublicInstance | null>(null)
const registerFormRef = ref<ComponentPublicInstance | null>(null)
const loading = ref(false)
const registerLoading = ref(false)
const showRegister = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const submit = async () => {
  if (!formRef.value) return
  
  try {
    await (formRef.value as any).validate()
    loading.value = true
    error.value = ''
    
    const response = await authApi.login(form.username, form.password)
    const token = response.data.access_token
    
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    emit('login', token)
    ElMessage.success('登录成功')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}

const register = async () => {
  if (!registerFormRef.value) return
  
  try {
    await (registerFormRef.value as any).validate()
    registerLoading.value = true
    
    await authApi.register(registerForm)
    ElMessage.success('注册成功，请登录')
    showRegister.value = false
    registerForm.username = ''
    registerForm.email = ''
    registerForm.password = ''
    registerForm.confirmPassword = ''
  } catch (err: any) {
    const detail = err.response?.data?.detail || '注册失败'
    ElMessage.error(detail)
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.register-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.register-dialog :deep(.el-dialog__footer) {
  padding: 16px 24px;
}
</style>