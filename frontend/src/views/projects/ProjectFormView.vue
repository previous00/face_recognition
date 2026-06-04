<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">{{ isEdit ? '编辑项目' : '新建项目' }}</h2>
    <el-card style="max-width: 800px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="项目名称" prop="title">
          <el-input v-model="form.title" placeholder="项目名称" />
        </el-form-item>
        <el-form-item label="负责人" prop="principal_investigator">
          <el-input v-model="form.principal_investigator" placeholder="项目负责人" />
        </el-form-item>
        <el-form-item label="项目描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="项目描述" />
        </el-form-item>
        <el-form-item label="资助来源">
          <el-input v-model="form.funding_source" placeholder="资助来源" />
        </el-form-item>
        <el-form-item label="经费(万元)">
          <el-input-number v-model="form.budget" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="规划中" value="planning" />
            <el-option label="进行中" value="active" />
            <el-option label="已完成" value="completed" />
            <el-option label="已暂停" value="suspended" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '提交' }}
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProject, createProject, updateProject } from '@/api/projects'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  principal_investigator: '',
  description: '',
  funding_source: '',
  budget: null,
  status: 'planning',
  start_date: '',
  end_date: '',
})

const rules = {
  title: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  principal_investigator: [{ required: true, message: '请输入负责人', trigger: 'blur' }],
  end_date: [{
    validator: (rule, value, callback) => {
      if (value && form.start_date && value < form.start_date) {
        callback(new Error('结束时间不能早于开始时间'))
      } else {
        callback()
      }
    },
    trigger: 'change',
  }],
  start_date: [{
    validator: (rule, value, callback) => {
      if (value && form.end_date && value > form.end_date) {
        callback(new Error('开始时间不能晚于结束时间'))
      } else {
        if (form.end_date) formRef.value?.validateField('end_date')
        callback()
      }
    },
    trigger: 'change',
  }],
}

onMounted(async () => {
  if (isEdit.value) {
    const res = await getProject(route.params.id)
    Object.assign(form, {
      title: res.data.title,
      principal_investigator: res.data.principal_investigator,
      description: res.data.description,
      funding_source: res.data.funding_source,
      budget: res.data.budget,
      status: res.data.status,
      start_date: res.data.start_date,
      end_date: res.data.end_date,
    })
  }
})

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const data = { ...form }
    if (!data.budget) delete data.budget
    if (!data.start_date) delete data.start_date
    if (!data.end_date) delete data.end_date
    if (isEdit.value) {
      await updateProject(route.params.id, data)
      ElMessage.success('修改成功')
    } else {
      await createProject(data)
      ElMessage.success('创建成功')
    }
    router.push('/projects')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}
</script>
