<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">{{ isEdit ? '编辑论文' : '添加论文' }}</h2>
    <el-card style="max-width: 800px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="论文标题" />
        </el-form-item>
        <el-form-item label="作者" prop="authors">
          <el-input v-model="form.authors" placeholder="多个作者用逗号分隔" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.abstract" type="textarea" :rows="4" placeholder="论文摘要" />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="form.keywords" placeholder="多个关键词用逗号分隔" />
        </el-form-item>
        <el-form-item label="发表日期">
          <el-date-picker v-model="form.publication_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="来源期刊">
          <el-input v-model="form.source_journal" placeholder="期刊名称" />
        </el-form-item>
        <el-form-item label="DOI">
          <el-input v-model="form.doi" placeholder="DOI标识符" />
        </el-form-item>
        <el-form-item label="上传文件">
          <el-upload
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".pdf,.doc,.docx"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 PDF、DOC、DOCX 格式</div>
            </template>
          </el-upload>
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
import { getPaper, createPaper, updatePaper } from '@/api/papers'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const fileList = ref([])

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  authors: '',
  abstract: '',
  keywords: '',
  publication_date: '',
  source_journal: '',
  doi: '',
  file: null,
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  authors: [{ required: true, message: '请输入作者', trigger: 'blur' }],
}

onMounted(async () => {
  if (isEdit.value) {
    const res = await getPaper(route.params.id)
    Object.assign(form, {
      title: res.data.title,
      authors: res.data.authors,
      abstract: res.data.abstract,
      keywords: res.data.keywords,
      publication_date: res.data.publication_date,
      source_journal: res.data.source_journal,
      doi: res.data.doi,
    })
  }
})

const handleFileChange = (file) => {
  form.file = file.raw
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const formData = new FormData()
    Object.keys(form).forEach(key => {
      if (form[key] !== null && form[key] !== '' && form[key] !== undefined) {
        formData.append(key, form[key])
      }
    })
    if (isEdit.value) {
      await updatePaper(route.params.id, formData)
      ElMessage.success('修改成功')
    } else {
      await createPaper(formData)
      ElMessage.success('添加成功')
    }
    router.push('/papers')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}
</script>
