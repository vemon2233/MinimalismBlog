<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 pt-24 pb-12">
      <!-- 数据加载完成后的状态 -->
      <div v-if="dataLoaded">
        <!-- 错误状态 -->
        <ApiErrorState v-if="apiError" @retry="loadProjectData" />
        <div v-else>
          <!-- 项目介绍部分 -->
          <section class="pt-20 pb-10 bg-gradient-to-r from-indigo-50 to-purple-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div class="bg-white rounded-xl shadow-md overflow-hidden">
                <div class="md:flex">
                  <!-- 项目封面图片 -->
                  <div class="md:flex-shrink-0 md:w-1/3">
                    <img class="h-full w-full object-cover object-center"
                      src="https://ai-public.mastergo.com/ai/img_res/fda1093c79b4c1dbcecb65102f40bbd2.jpg"
                      alt="Project Cover" />
                  </div>
                  <!-- 项目信息 -->
                  <div class="p-8 md:w-2/3">
                    <div class="uppercase tracking-wide text-sm text-indigo-500 font-semibold">项目</div>
                    <h1 class="mt-1 text-3xl font-bold text-gray-900">{{ project.name }}</h1>
                    <p class="mt-2 text-gray-600">{{ project.description || '暂无项目描述' }}</p>
                    <div class="mt-4 flex items-center">
                      <el-icon>
                        <Calendar />
                      </el-icon>
                      <span class="ml-2 text-gray-500">创建于 {{ formatDate(project.created_at) }}</span>
                    </div>
                    <div class="mt-2 flex items-center">
                      <el-icon>
                        <Document />
                      </el-icon>
                      <span class="ml-2 text-gray-500">包含 {{ project.article_count || 0 }} 篇文章</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 文章列表部分 -->
          <div class="max-w-7xl mx-auto px-4 pt-8 pb-12">


            <!-- 无文章状态 -->
            <div v-if="project.articles && project.articles.length === 0"
              class="bg-white rounded-lg shadow-sm p-8 text-center">
              <el-icon class="text-gray-400 text-4xl mb-4">
                <Document />
              </el-icon>
              <h3 class="text-xl font-bold text-gray-800 mb-2">暂无文章</h3>
              <p class="text-gray-600">该项目目前还没有关联的文章</p>
            </div>

            <!-- 有文章状态 -->
            <div v-else class="space-y-6">
              <h2 class="text-2xl font-bold text-gray-900 mb-6">项目文章</h2>
              <SingleArticle v-for="article in project.articles" :key="article.id" :article="{
                id: article.id,
                title: article.title,
                created_at: article.created_at,
                read_time: 5, // 默认值，实际应该从API获取
                view_count: 0, // 默认值
                like_count: 0, // 默认值
                comment_count: 0, // 默认值
                excerpt: article.excerpt || '',
                tags: [] // 项目文章可能没有标签，或者可以从API获取
              }" @article-click="goToArticle" />
            </div>
          </div>
        </div>
      </div>

      <!-- 数据加载中 -->
      <div v-else>
        <!-- 数据加载完成前显示空白 -->
      </div>
    </div>
  </div>
</template>

<route>
{
  meta: {
    title: "项目详情 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Calendar, Document, Loading } from '@element-plus/icons-vue';
import SingleArticle from '../../components/SingleArticle.vue';
import ApiErrorState from '../../components/ApiErrorState.vue';
import { programService } from '../../apis';

const route = useRoute();
const router = useRouter();

const project = ref({
  id: 0,
  name: '',
  description: '',
  created_at: '',
  updated_at: '',
  article_count: 0,
  articles: []
});
const dataLoaded = ref(false);
const apiError = ref(false);

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知日期';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 加载项目数据
const loadProjectData = async () => {
  dataLoaded.value = false;
  apiError.value = false;

  try {
    const projectId = route.params.id;

    // 调用后端的项目API
    const response = await programService.getProject(projectId);
    project.value = response;

  } catch (error) {
    console.error('加载项目数据失败:', error);
    apiError.value = true;
  } finally {
    dataLoaded.value = true;
  }
};

// 跳转到文章详情页
const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`);
};

// 监听路由变化
watch(
  () => route.params.id,
  () => {
    loadProjectData();
  }
);

// 页面加载时初始化
onMounted(() => {
  loadProjectData();
});
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>
