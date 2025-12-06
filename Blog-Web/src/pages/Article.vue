<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 文章内容区 -->
    <main class="max-w-4xl mx-auto px-4 pt-30 pb-12">
      <div v-if="loading" class="bg-white rounded-lg shadow-sm p-8 text-center">
        <el-icon class="text-4xl text-gray-400 animate-spin"><Loading /></el-icon>
        <p class="mt-4 text-gray-600">加载中...</p>
      </div>
      
      <div v-else-if="article">
        <article class="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ article.title }}</h1>
          <div class="flex items-center text-gray-500 text-sm mb-8 space-x-6">
            <span class="flex items-center">
              <el-icon><Calendar /></el-icon>
              <span class="ml-2">{{ formatDate(article.created_at) }}</span>
            </span>
            <span class="flex items-center">
              <el-icon><Timer /></el-icon>
              <span class="ml-2">{{ article.read_time }}</span>
            </span>
            <div class="flex gap-2">
              <el-tag 
                v-for="tag in article.tags" 
                :key="tag" 
                size="small"
                class="!rounded-button"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
          <div class="prose max-w-none">
            <p class="text-gray-700 leading-relaxed mb-6 text-lg">{{ article.excerpt }}</p>
            <div class="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {{ article.content }}
            </div>
          </div>
        </article>
        <!-- 评论区 -->
        <Comment />
      </div>
      
      <div v-else class="bg-white rounded-lg shadow-sm p-8 text-center">
        <el-icon class="text-4xl text-gray-400"><Warning /></el-icon>
        <h2 class="mt-4 text-xl font-bold text-gray-800">文章未找到</h2>
        <p class="mt-2 text-gray-600">抱歉，您要查看的文章不存在或已被删除。</p>
        <el-button @click="goBack" class="mt-4 !rounded-button">
          <el-icon class="mr-2"><ArrowLeft /></el-icon>
          返回首页
        </el-button>
      </div>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Calendar, Timer, ArrowLeft, Loading, Warning } from '@element-plus/icons-vue';
import { articleService } from '../apis';

const route = useRoute();
const router = useRouter();

const article = ref(null);
const loading = ref(true);

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 加载文章详情
const loadArticle = async () => {
  loading.value = true;
  try {
    const articleId = route.params.id;
    const response = await articleService.getArticle(articleId);
    article.value = response.article;
  } catch (error) {
    console.error('加载文章失败:', error);
    article.value = null;
  } finally {
    loading.value = false;
  }
};

// 返回首页
const goBack = () => {
  router.push('/home');
};

onMounted(() => {
  loadArticle();
});
</script>

<style scoped>
.prose {
  max-width: none;
}

.prose img {
  margin: 0;
}
</style>
