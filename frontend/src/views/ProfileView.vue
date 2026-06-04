<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">个人资料</h2>
    <el-card style="max-width: 600px">
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="用户名">
          <el-input :value="form.username" disabled />
        </el-form-item>
        <el-form-item label="角色">
          <el-tag>{{ { super_admin: '超级管理员', admin: '管理员', user: '普通用户' }[form.role] || form.role }}</el-tag>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="所属机构">
          <el-input v-model="form.institution" />
        </el-form-item>
        <el-form-item label="研究方向">
          <el-input v-model="form.research_field" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="form.bio" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSave">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getProfile, updateProfile } from '@/api/auth'
import { ElMessage } from 'element-plus'

const form = reactive({
  username: '',
  email: '',
  phone: '',
  institution: '',
  research_field: '',
  bio: '',
  role: '',
})
const loading = ref(false)

onMounted(async () => {
  const res = await getProfile()
  Object.assign(form, res.data)
})

const handleSave = async () => {
  loading.value = true
  try {
    await updateProfile({
      email: form.email,
      phone: form.phone,
      institution: form.institution,
      research_field: form.research_field,
      bio: form.bio,
    })
    ElMessage.success('保存成功')
  } catch (err) {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}
</script>
