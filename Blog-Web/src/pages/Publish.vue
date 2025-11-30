<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区 -->
    <div class="max-w-5xl mx-auto px-4 pt-24 pb-20">
      <div class="bg-white rounded-lg shadow-sm p-8">
        <!-- 页面标题和操作按钮 -->
        <div class="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">
          <h1 class="text-2xl font-bold text-gray-800">发布新文章</h1>
          <div class="flex gap-4">
            <el-button @click="goBack" class="!rounded-button">
              <el-icon class="mr-2"><ArrowLeft /></el-icon>
              返回
            </el-button>
            <el-button 
              type="primary" 
              @click="handlePublish"
              :loading="submitting"
              class="!rounded-button"
            >
              <el-icon class="mr-2"><Check /></el-icon>
              发布文章
            </el-button>
          </div>
        </div>

        <div class="space-y-6">
          <!-- 标题 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标题</label>
            <el-input
              v-model="articleForm.title"
              placeholder="请输入文章标题..."
              maxlength="100"
              show-word-limit
              class="text-xl font-bold"
              :class="{ 'border-red-300': errors.title }"
            />
            <div v-if="errors.title" class="text-red-500 text-sm mt-2">{{ errors.title }}</div>
          </div>

          <!-- 内容 -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-gray-700">内容</label>
              <span class="text-xs text-gray-500">{{ articleForm.content.length }} 字符</span>
            </div>
            <el-input
              v-model="articleForm.content"
              type="textarea"
              :rows="15"
              placeholder="请输入文章内容..."
              maxlength="8000"
              show-word-limit
              :class="{ 'border-red-300': errors.content }"
            />
            <div v-if="errors.content" class="text-red-500 text-sm mt-2">{{ errors.content }}</div>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
            <el-select
              v-model="articleForm.tags"
              multiple
              filterable
              allow-create
              default-first-option
              :reserve-keyword="false"
              placeholder="选择或输入文章标签"
              class="w-full"
            >
              <el-option
                v-for="tag in allTags"
                :key="tag"
                :label="tag"
                :value="tag"
              />
            </el-select>
          </div>

          <!-- 阅读时间 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">阅读时间（分钟）</label>
            <el-input
              v-model="articleForm.readTime"
            />
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
    title: "发布文章 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, Check } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { articleService } from '../services/api';

const router = useRouter();

// 表单数据
const articleForm = reactive({
  title: '',
  content: '',
  tags: [] as string[],
  readTime: 5  // 默认5分钟
});

// 错误信息
const errors = reactive({
  title: '',
  content: ''
});

// 提交状态
const submitting = ref(false);
const submitError = ref('');
const allTags = ref([]);

// 加载所有标签
const loadAllTags = async () => {
  try {
    const response = await articleService.getTags();
    allTags.value = response.tags || [];
  } catch (error) {
    console.error('加载标签失败:', error);
    allTags.value = [];
  }
};

// 页面加载时获取标签
onMounted(() => {
  loadAllTags();
});

// 验证表单
const validateForm = () => {
  let isValid = true;
  
  // 重置错误信息
  errors.title = '';
  errors.content = '';
  submitError.value = '';

  // 验证标题
  if (!articleForm.title.trim()) {
    errors.title = '标题不能为空';
    isValid = false;
  } else if (articleForm.title.trim().length < 3) {
    errors.title = '标题至少需要3个字符';
    isValid = false;
  }

  // 验证内容
  if (!articleForm.content.trim()) {
    errors.content = '内容不能为空';
    isValid = false;
  } else if (articleForm.content.trim().length < 10) {
    errors.content = '内容至少需要10个字符';
    isValid = false;
  }

  return isValid;
};

// 发布文章
const handlePublish = async () => {
  if (!validateForm()) return;

  submitting.value = true;

  try {
    console.log('提交的标签数据:', articleForm.tags);
    
    await articleService.createArticle({
      title: articleForm.title.trim(),
      excerpt: articleForm.content.slice(0, 150).replace(/[#*`]/g, '') + '...',
      content: articleForm.content.trim(),
      read_time: articleForm.readTime || 5,
      tags: articleForm.tags,
      is_published: true
    });

    ElMessage.success('文章发布成功！');
    router.push('/home');
    
  } catch (error) {
    console.error('发布文章失败:', error);
    console.error('错误详情:', error.response?.data);
    submitError.value = '发布文章失败，请重试';
  } finally {
    submitting.value = false;
  }
};

// 返回
const goBack = () => {
  router.push('/home');
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

:deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}

:deep(.el-textarea__inner) {
  border: 1px solid #e5e7eb !important;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05) !important;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
  line-height: 1.7 !important;
}

:deep(.el-textarea__inner:focus) {
  border-color: #57534e !important;
  box-shadow: 0 0 0 1px #57534e !important;
}
</style>
