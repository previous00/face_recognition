<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2>用户注册</h2>
      <el-form :model="form" @submit.prevent="handleRegister">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.email" placeholder="邮箱" prefix-icon="Message" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.nickname" placeholder="昵称（选填）" prefix-icon="UserFilled" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码（至少6位）" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password2" type="password" placeholder="确认密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%;">注册</el-button>
        </el-form-item>
      </el-form>
      <p class="link">已有账号？<router-link to="/login">去登录</router-link></p>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const form = ref({ username: '', email: '', nickname: '', password: '', password2: '' })

async function handleRegister() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请填写必要信息')
    return
  }
  if (form.value.password !== form.value.password2) {
    ElMessage.warning('两次密码不一致')
    return
  }
  loading.value = true
  try {
    await userStore.register(form.value)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    const msg = e.response?.data
    if (msg?.username) ElMessage.error(`用户名: ${msg.username[0]}`)
    else ElMessage.error('注册失败，请检查信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page { display: flex; justify-content: center; padding-top: 60px; }
.register-card { width: 400px; }
.register-card h2 { text-align: center; margin-bottom: 24px; }
.link { text-align: center; color: #666; font-size: 14px; }
.link a { color: #409eff; }
</style>
