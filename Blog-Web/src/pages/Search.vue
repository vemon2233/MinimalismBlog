<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 pt-24 pb-12">
      <!-- 搜索头部 -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">搜索结果</h1>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文章..."
              :prefix-icon="Search"
              @keyup.enter="handleSearch"
              size="large"
            />
          </div>
          <el-button type="primary" size="large" @click="handleSearch">
            <el-icon class="mr-1">
              <Search />
            </el-icon>
            搜索
          </el-button>
        </div>
        <div v-if="searchQuery" class="mt-4 text-gray-600">
          搜索关键词: <span class="font-semibold text-blue-600">{{ searchQuery }}</span>
          <span class="ml-4">找到 {{ totalResults }} 条结果</span>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div v-if="dataLoaded">
        <!-- 错误状态 -->
        <div v-if="apiError" class="bg-white rounded-lg shadow-sm p-8 text-center">
          <el-icon class="text-red-500 text-4xl mb-4">
            <Warning />
          </el-icon>
          <h3 class="text-xl font-bold text-gray-800 mb-2">服务异常</h3>
          <p class="text-gray-600 mb-4">无法连接到服务器，请检查网络连接或稍后重试</p>
          <el-button type="primary" @click="loadSearchResults">
            <el-icon class="mr-1">
              <Refresh />
            </el-icon>
            重新加载
          </el-button>
        </div>
        
        <!-- 无结果状态 -->
        <div v-else-if="searchResults.length === 0" class="bg-white rounded-lg shadow-sm p-8 text-center">
          <el-icon class="text-gray-400 text-4xl mb-4">
            <Document />
          </el-icon>
          <h3 class="text-xl font-bold text-gray-800 mb-2">未找到相关文章</h3>
          <p class="text-gray-600">请尝试使用其他关键词搜索</p>
        </div>
        
        <!-- 有结果状态 -->
        <div v-else class="space-y-6">
          <article 
            v-for="article in searchResults" 
            :key="article.id"
            class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer"
            @click="goToArticle(article.id)"
          >
            <h2 class="text-xl font-bold mb-2 hover:text-stone-600 transition-colors">{{ article.title }}</h2>
            <div class="flex items-center text-sm text-gray-500 mb-3 space-x-4">
              <span class="flex items-center">
                <el-icon class="mr-1">
                  <Calendar />
                </el-icon>
                {{ article.created_at }}
              </span>
              <span class="flex items-center">
                <el-icon class="mr-1">
                  <Timer />
                </el-icon>
                {{ formatReadTime(article.read_time) }}
              </span>
              <span class="flex items-center">
                <el-icon class="mr-1">
                  <View />
                </el-icon>
                {{ article.view_count || 0 }}
              </span>
              <span class="flex items-center">
                <el-icon class="mr-1">
                  <Star />
                </el-icon>
                {{ article.like_count || 0 }}
              </span>
              <span class="flex items-center">
                <el-icon class="mr-1">
                  <ChatDotRound />
                </el-icon>
                {{ article.comment_count || 0 }}
              </span>
            </div>
            <p class="text-gray-600 mb-4 line-clamp-3">{{ article.excerpt }}</p>
            <div class="flex flex-wrap gap-2">
              <el-tag 
                v-for="tag in article.tags" 
                :key="tag" 
                class="!rounded-button cursor-pointer"
                @click.stop="searchByTag(tag)"
              >
                {{ tag }}
              </el-tag>
            </div>
          </article>
          
          <!-- 分页 -->
          <div class="mt-8 flex justify-center">
            <el-pagination 
              v-model:current-page="currentPage" 
              :page-size="10" 
              :total="totalResults"
              layout="prev, pager, next" 
              @current-change="handlePageChange" 
            />
          </div>
        </div>
      </div>
      
      <!-- 数据加载中 -->
      <div v-else class="flex justify-center items-center py-12">
        <el-icon class="text-4xl text-blue-500 animate-spin">
          <Loading />
        </el-icon>
        <span class="ml-2 text-gray-600">搜索中...</span>
      </div>
    </div>
    
    <!-- 回到顶部 -->
    <el-backtop :right="20" :bottom="20" />
  </div>
</template>

<route>
{
  meta: {
    title: "搜索结果 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  Search, 
  Warning, 
  Refresh, 
  Document, 
  Calendar, 
  Timer, 
  View, 
  Star, 
  ChatDotRound,
  Loading 
} from '@element-plus/icons-vue';
import { articleService } from '../services/api';

const route = useRoute();
const router = useRouter();

const searchQuery = ref('');
const currentPage = ref(1);
const searchResults = ref([]);
const totalResults = ref(0);
const dataLoaded = ref(false);
const apiError = ref(false);

// 从路由参数获取搜索关键词
const getSearchQueryFromRoute = () => {
  const query = route.query.q as string;
  if (query) {
    searchQuery.value = query;
  }
};

// 加载搜索结果
const loadSearchResults = async () => {
  if (!searchQuery.value.trim()) return;
  
  dataLoaded.value = false;
  apiError.value = false;
  
  try {
    const response = await articleService.searchArticles({
      query: searchQuery.value,
      page: currentPage.value,
      per_page: 10
    });
    
    searchResults.value = response.articles;
    totalResults.value = response.total;
    
  } catch (error) {
    console.error('搜索失败:', error);
    apiError.value = true;
    searchResults.value = [];
    totalResults.value = 0;
  } finally {
    dataLoaded.value = true;
  }
};

// 处理搜索
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    currentPage.value = 1;
    // 更新URL参数
    router.push({
      path: '/search',
      query: {
        q: searchQuery.value.trim()
      }
    });
    loadSearchResults();
  }
};

// 按标签搜索
const searchByTag = (tag: string) => {
  searchQuery.value = tag;
  handleSearch();
};

// 跳转到文章详情页
const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`);
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

// 页码变化处理
const handlePageChange = () => {
  loadSearchResults();
};

// 监听路由变化
watch(
  () => route.query.q,
  (newQuery) => {
    if (newQuery) {
      searchQuery.value = newQuery as string;
      currentPage.value = 1;
      loadSearchResults();
    }
  }
);

// 页面加载时初始化
onMounted(() => {
  getSearchQueryFromRoute();
  if (searchQuery.value) {
    loadSearchResults();
  } else {
    dataLoaded.value = true;
  }
});
</script>

<style scoped>
.el-pagination :deep(.el-pager li.is-active) {
  background-color: #3b82f6;
  color: white;
}

.el-pagination :deep(.el-pager li:hover) {
  color: #3b82f6;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
