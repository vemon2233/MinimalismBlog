<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 文章内容区 -->
    <main class="max-w-4xl mx-auto px-4 pt-24 pb-12">
      <!-- 数据加载完成后的状态 -->
      <div v-if="dataLoaded">
        <div v-if="article">
          <article class="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ article.title }}</h1>
            <div class="flex items-center text-gray-500 text-sm mb-8 space-x-6">
              <span class="flex items-center">
                <el-icon>
                  <Calendar />
                </el-icon>
                <span class="ml-2">{{ formatDate(article.created_at) }}</span>
              </span>
              <span class="flex items-center">
                <el-icon>
                  <Timer />
                </el-icon>
                <span class="ml-2">{{ formatReadTime(article.read_time) }}</span>
              </span>
              <span class="flex items-center cursor-pointer" @click="handleLike">
                <el-icon :class="isLiked ? 'liked-icon' : 'unliked-icon'" class="transition-colors">
                  <StarFilled v-if="isLiked" />
                  <Star v-else />
                </el-icon>
                <span class="ml-2">{{ likeCount }}</span>
              </span>
              <div class="flex gap-2">
                <el-tag v-for="tag in article.tags" :key="tag" size="small" class="!rounded-button">
                  {{ tag }}
                </el-tag>
              </div>
            </div>
            <div class="prose max-w-none">
              <div class="text-gray-700 leading-relaxed whitespace-pre-wrap">
                {{ article.content }}
              </div>
            </div>
          </article>
          <!-- 评论区 -->
          <Comment :article-id="parseInt(route.params.id as string)" />
        </div>

        <div v-else class="bg-white rounded-lg shadow-sm p-8 text-center">
          <el-icon class="text-4xl text-gray-400">
            <Warning />
          </el-icon>
          <h2 class="mt-4 text-xl font-bold text-gray-800">文章未找到</h2>
          <p class="mt-2 text-gray-600">抱歉，您要查看的文章不存在或已被删除。</p>
          <el-button @click="goBack" class="mt-4 !rounded-button">
            <el-icon class="mr-2">
              <ArrowLeft />
            </el-icon>
            返回首页
          </el-button>
        </div>
      </div>
      
      <!-- 数据加载中：显示空白 -->
      <div v-else>
        <!-- 数据加载完成前显示空白 -->
      </div>
    </main>
  </div>
</template>

<route>
{
  meta: {
    title: "文章详情 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Calendar, Timer, ArrowLeft, Warning, Star, StarFilled } from '@element-plus/icons-vue';
import { articleService, statisticService } from '../../apis';

const route = useRoute();
const router = useRouter();

const article = ref(null);
const liking = ref(false);
const likeCount = ref(0);
const isLiked = ref(false); // 跟踪点赞状态
const dataLoaded = ref(false); // 标记数据是否已加载完成

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 格式化阅读时间
const formatReadTime = (minutes: number) => {
  if (minutes < 60) {
    return `${minutes} 分钟阅读`;
  } else {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    if (remainingMinutes === 0) {
      return `${hours} 小时阅读`;
    } else {
      return `${hours} 小时 ${remainingMinutes} 分钟阅读`;
    }
  }
};

// 加载文章详情和点赞数
const loadArticle = async () => {
  dataLoaded.value = false; // 重置数据加载状态
  try {
    const articleId = route.params.id;
    
    // 获取文章详情
    const articleResponse = await articleService.getArticle(articleId);
    article.value = articleResponse;
    
    // 获取文章列表数据来获取点赞数
    const articlesResponse = await articleService.getArticles();
    const currentArticle = articlesResponse.articles.find(a => a.id === parseInt(articleId));
    
    if (currentArticle) {
      likeCount.value = currentArticle.like_count;
      // 这里可以根据需要设置初始点赞状态
      // 在实际应用中，应该根据用户是否点赞过来设置 isLiked
    }
    
    // 标记数据加载完成
    dataLoaded.value = true;
  } catch (error) {
    article.value = null;
    // 即使出错也标记为已加载，以便显示错误状态
    dataLoaded.value = true;
  }
};

// 返回首页
const goBack = () => {
  router.push('/home');
};

// 增加浏览量
const incrementViewCount = async () => {
  try {
    const articleId = route.params.id;
    await statisticService.incrementViewCount(articleId);
  } catch (error) {
    console.error('增加浏览量失败:', error);
  }
};

// 处理点赞/取消点赞
const handleLike = async () => {
  if (liking.value) return;
  
  liking.value = true;
  try {
    const articleId = route.params.id;
    const action = isLiked.value ? 'unlike' : 'like';
    const response = await statisticService.toggleLikeCount(articleId, action);
    
    likeCount.value = response.like_count;
    isLiked.value = action === 'like';
  } catch (error) {
    console.error('点赞操作失败:', error);
  } finally {
    liking.value = false;
  }
};

onMounted(() => {
  loadArticle();
  incrementViewCount();
});
</script>

<style scoped>
.prose {
  max-width: none;
}

.prose img {
  margin: 0;
}

/* 点赞图标样式 - 使用高优先级选择器 */
.liked-icon {
  color: rgb(239 68 68) !important; /* text-red-500 */
}

.unliked-icon {
  color: rgb(107 114 128) !important; /* text-gray-500 */
}

.unliked-icon:hover {
  color: rgb(248 113 113) !important; /* text-red-400 */
}
</style>
