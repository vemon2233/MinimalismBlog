<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 pt-30 pb-20">
      <div class="bg-white rounded-lg shadow-sm p-10">
        <!-- 页面标题和操作按钮 -->
        <div class="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">
          <h1 class="text-2xl font-bold text-gray-800">新增项目</h1>
          <div class="flex gap-4">
            <el-button @click="goBack" class="!rounded-button">
              <el-icon class="mr-2">
                <ArrowLeft />
              </el-icon>
              返回
            </el-button>
            <el-button type="primary" plain @click="handleCreate" :loading="submitting" class="!rounded-button">
              <el-icon class="mr-2">
                <Check />
              </el-icon>
              创建项目
            </el-button>
          </div>
        </div>

        <div class="space-y-6">
          <!-- 上传图片 -->
          <div class="flex justify-center">
            <el-upload class="avatar-uploader" :action="uploadAction" :headers="uploadHeaders"
              :show-file-list="false" :on-success="handleUploadSuccess" :before-upload="beforeUpload"
              accept=".png,.jpg,.jpeg,.gif,.webp">
              <img v-if="projectForm.imagePreview" :src="projectForm.imagePreview"
                class="w-[500px] h-[332px] object-fill rounded-lg" />
              <div v-else
                class="w-[500px] h-[332px] flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors">
                <div class="text-center">
                  <el-icon class="text-4xl text-gray-400 mb-2">
                    <Plus />
                  </el-icon>
                  <p class="text-sm text-gray-500">点击上传图片</p>
                  <p class="text-xs text-gray-400 mt-1">支持 PNG、JPG、JPEG、GIF、WEBP</p>
                  <p class="text-xs text-gray-400">大小不超过 5MB</p>
                </div>
              </div>
            </el-upload>
          </div>

          <!-- 项目名称 -->
          <div class="px-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">项目名称</label>
            <el-input v-model="projectForm.name" placeholder="请输入项目名称..." maxlength="20" show-word-limit
              class="text-xl font-bold" :class="{ 'border-red-300': errors.name }" />
            <div v-if="errors.name" class="text-red-500 text-sm mt-2">{{ errors.name }}</div>
          </div>

          <!-- 项目描述 -->
          <div class="px-6 mb-10">
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-gray-700">项目描述</label>
              <span class="text-xs text-gray-500">{{ projectForm.description.length }} 字符</span>
            </div>
            <el-input v-model="projectForm.description" type="textarea" :rows="6" placeholder="请输入项目描述..."
              maxlength="200" show-word-limit :class="{ 'border-red-300': errors.description }" />
            <div v-if="errors.description" class="text-red-500 text-sm mt-2">{{ errors.description }}</div>
          </div>

          <!-- 错误提示 -->
          <div v-if="submitError" class="p-4 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100">
            {{ submitError }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<route>
{
  meta: {
    title: "新增项目 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, Check, Upload, Delete, Plus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { programService } from '../apis';

const router = useRouter();

// 表单数据
const projectForm = reactive({
  name: '',
  description: '',
  imageFile: null as File | null,
  imagePreview: '' as string
});

// 错误信息
const errors = reactive({
  name: '',
  description: ''
});

// 提交状态
const submitting = ref(false);
const submitError = ref('');

// 上传配置
const uploadAction = ref('/api/program/create'); // 后端API地址
const uploadHeaders = ref({
  'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
});

// 验证表单
const validateForm = () => {
  let isValid = true;

  // 重置错误信息
  errors.name = '';
  errors.description = '';
  submitError.value = '';

  // 验证项目名称
  if (!projectForm.name.trim()) {
    errors.name = '项目名称不能为空';
    isValid = false;
  } else if (projectForm.name.trim().length < 2) {
    errors.name = '项目名称至少需要2个字符';
    isValid = false;
  }

  // 验证项目描述（可选）
  if (projectForm.description.trim().length > 500) {
    errors.description = '项目描述不能超过500个字符';
    isValid = false;
  }

  return isValid;
};

// 上传前验证
const beforeUpload = (file: File) => {
  const isImage = /\.(png|jpg|jpeg|gif|webp)$/i.test(file.name);
  const isLt5M = file.size / 1024 / 1024 < 5;

  if (!isImage) {
    ElMessage.error('只能上传图片文件！');
    return false;
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过5MB！');
    return false;
  }

  // 保存文件
  projectForm.imageFile = file;

  // 创建预览
  const reader = new FileReader();
  reader.onload = (e) => {
    projectForm.imagePreview = e.target?.result as string;
  };
  reader.readAsDataURL(file);

  return false; // 返回false，手动上传
};

// 处理上传成功
const handleUploadSuccess = (response: any) => {
  // 这里不需要处理，因为我们手动上传
};

// 处理上传错误
const handleUploadError = (error: any) => {
  console.error('上传失败:', error);
  ElMessage.error('图片上传失败，请重试');
};

// 移除图片
const removeImage = () => {
  projectForm.imageFile = null;
  projectForm.imagePreview = '';
};

// 创建项目
const handleCreate = async () => {
  if (!validateForm()) return;

  submitting.value = true;
  submitError.value = '';

  try {
    // 创建FormData对象
    const formData = new FormData();
    formData.append('name', projectForm.name.trim());
    formData.append('description', projectForm.description.trim());

    // 如果有图片文件，添加到FormData
    if (projectForm.imageFile) {
      formData.append('image', projectForm.imageFile);
    }

    // 调用API创建项目
    const response = await programService.createProject(formData);

    ElMessage.success('项目创建成功！');

    // 跳转到项目列表页面
    router.push('/program');

  } catch (error: any) {
    console.error('创建项目失败:', error);
    submitError.value = error.response?.data?.error || '创建项目失败，请重试';
    ElMessage.error(submitError.value);
  } finally {
    submitting.value = false;
  }
};

// 返回
const goBack = () => {
  router.back();
};
</script>

<style scoped>
</style>
