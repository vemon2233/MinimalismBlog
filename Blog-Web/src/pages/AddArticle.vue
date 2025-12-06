<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 pt-30 pb-20">
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
              plain
              @click="handlePublish"
              :loading="submitting"
              class="!rounded-button"
            >
              <el-icon class="mr-2"><Check /></el-icon>
              发布文章
            </el-button>
          </div>
        </div>

        <!-- 使用EditArticle组件 -->
        <EditArticle
          ref="editArticleRef"
          :submitting="submitting"
          :initial-data="{
            title: '',
            content: '',
            tags: [],
            readTime: 5,
            programId: programIdFromRoute
          }"
          @update:submitting="submitting = $event"
          @submit="handleSubmit"
        />
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
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ArrowLeft, Check } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { articleService, programService } from '../apis';
import EditArticle from '../components/EditArticle.vue';

const router = useRouter();
const route = useRoute();

// 编辑文章组件引用
const editArticleRef = ref();

// 提交状态
const submitting = ref(false);

// 从路由参数中获取program_id
const programIdFromRoute = ref<number | null>(null);

// 初始化：从路由参数中获取program_id
onMounted(() => {
  const programId = route.query.program_id;
  if (programId) {
    programIdFromRoute.value = parseInt(programId as string);
  }
});

// 处理表单提交
const handleSubmit = async (articleData: any) => {
  try {
    // 提取program_id（如果有）
    const programId = articleData.program_id;
    // 从articleData中移除program_id，因为article/create接口不需要它
    const articleDataForCreate = { ...articleData };
    delete articleDataForCreate.program_id;
    
    // 调用API创建文章
    const response = await articleService.createArticle(articleDataForCreate);
    const articleId = response.article_id;
    
    // 如果选择了项目，将文章关联到项目
    if (programId) {
      try {
        await programService.addArticleToProject(programId, articleId);
      } catch (projectError) {
        ElMessage.warning('文章创建成功，但关联到项目失败');
      }
    }
    ElMessage.success('文章发布成功！');
    router.push('/home');
    
  } catch (error) {
    console.error('发布文章失败:', error);
    console.error('错误详情:', error.response?.data);
    // 错误信息已经在EditArticle组件中显示
  } finally {
    submitting.value = false;
  }
};

// 发布文章
const handlePublish = async () => {
  if (editArticleRef.value) {
    // 调用EditArticle组件的提交方法
    const success = await editArticleRef.value.submitForm();
    if (success) {
      // 提交成功，handleSubmit会被调用
      return;
    }
  }
};

// 返回
const goBack = () => {
  router.back();
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
