<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 pt-24 pb-12">
      <!-- 分类导航栏（整合分类方式和标签页） -->
      <div class="bg-gray-50 border-b">
        <div class="max-w-7xl mx-auto px-4 py-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <!-- 分类方式选择（使用Radio） -->
            <div class="flex items-start">
              <el-radio-group v-model="categoryType" size="small" class="flex space-y-2">
                <el-radio value="tag">按标签</el-radio>
                <el-radio value="year">按年份</el-radio>
              </el-radio-group>
            </div>

            <!-- 顶部分类导航 -->
            <div class="w-full overflow-x-auto scrollbar-hide">
              <!-- 进一步缩小网格间距 -->
              <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-1.5 min-w-max">
                <div v-for="category in categories" :key="category.id" :class="[
                  'flex flex-col items-center px-3 py-2 rounded-lg transition-all cursor-pointer hover:shadow-md',
                  activeCategory === category.id ? 'bg-white shadow-md ring-1 ring-blue-100' : 'bg-white/60 hover:bg-white'
                ]" @click="activeCategory = category.id">
                  <!-- 横向压缩文字和间距 -->
                  <span class="text-sm font-medium mb-0.5 whitespace-nowrap"
                    :class="activeCategory === category.id ? 'text-blue-600' : 'text-gray-700'">
                    {{ category.name }}
                  </span>
                  <span class="text-xs text-gray-400">
                    {{ category.count }}篇
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 主要内容区域 -->
      <main class="max-w-7xl mx-auto px-4 py-8">
        <!-- 错误状态 -->
        <div v-if="apiError" class="bg-white rounded-lg shadow-sm p-8 text-center">
          <el-icon class="text-red-500 text-4xl mb-4">
            <Warning />
          </el-icon>
          <h3 class="text-xl font-bold text-gray-800 mb-2">服务异常</h3>
          <p class="text-gray-600 mb-4">无法连接到服务器，请检查网络连接或稍后重试</p>
          <el-button type="primary" @click="loadData">
            <el-icon class="mr-1">
              <Refresh />
            </el-icon>
            重新加载
          </el-button>
        </div>
        
        <!-- 数据加载完成后的状态 -->
        <div v-else-if="dataLoaded">
          <!-- 无数据状态 -->
          <div v-if="categories.length === 0" class="bg-white rounded-lg shadow-sm p-8 text-center">
            <el-icon class="text-gray-400 text-4xl mb-4">
              <Document />
            </el-icon>
            <h3 class="text-xl font-bold text-gray-800 mb-2">暂无文章</h3>
            <p class="text-gray-600">当前分类下没有找到相关文章</p>
          </div>
          
          <!-- 正常状态：有分类数据 -->
          <div v-else>
            <div v-for="category in categories" :key="category.id" class="mb-12">
              <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900 border-b-2 border-blue-500 pb-2 inline-block">
                  {{ category.name }}
                </h2>
              </div>
              <div class="space-y-4">
                <div v-for="article in category.articles" :key="article.id" 
                  class="flex items-center group cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors"
                  @click="goToArticle(article.id)">
                  <span class="w-32 text-sm text-gray-400">{{ article.date }}</span>
                  <span class="text-gray-700 hover:text-blue-600 transition-colors">{{ article.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 数据加载中：显示空白 -->
        <div v-else>
          <!-- 数据加载完成前显示空白 -->
        </div>
      </main>
    </div>
  </div>
</template>

<route>
{
  meta: {
    title: "文章归档 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Warning, Refresh, Document } from '@element-plus/icons-vue';
import { articleService } from '../services/api';

const router = useRouter();

const categoryType = ref('tag');
const activeCategory = ref('');
const dataLoaded = ref(false);
const apiError = ref(false);
const allArticles = ref([]);
const allTags = ref([]);

// 加载数据
const loadData = async () => {
  dataLoaded.value = false;
  apiError.value = false;
  try {
    // 并行加载文章和标签数据
    const [articlesResponse, tagsResponse] = await Promise.all([
      articleService.getArticles(),
      articleService.getTags()
    ]);

    allArticles.value = articlesResponse.articles;
    allTags.value = tagsResponse.tags;

    // 设置默认激活的分类
    if (allTags.value.length > 0) {
      activeCategory.value = allTags.value[0];
    }

  } catch (error) {
    console.error('加载数据失败:', error);
    apiError.value = true;
    allArticles.value = [];
    allTags.value = [];
  } finally {
    dataLoaded.value = true;
  }
};

// 页面加载时获取数据
onMounted(() => {
  loadData();
});

// 标签分类数据
const tagCategories = computed(() => {
  if (!allTags.value.length) return [];

  return allTags.value.map(tag => {
    const articles = allArticles.value.filter(article => 
      article.tags && article.tags.includes(tag)
    );
    
    return {
      id: tag,
      name: tag,
      count: articles.length,
      articles: articles.map(article => ({
        id: article.id,
        date: article.created_at,
        title: article.title
      }))
    };
  }).filter(category => category.count > 0);
});

// 年份分类数据
const yearCategories = computed(() => {
  const yearMap = new Map();
  
  // 从所有文章中按年份重新组织
  allArticles.value.forEach(article => {
    const year = article.created_at ? article.created_at.split('-')[0] : '未知';
    if (!yearMap.has(year)) {
      yearMap.set(year, {
        id: year,
        name: `${year}年`,
        count: 0,
        articles: []
      });
    }
    const yearData = yearMap.get(year);
    yearData.articles.push({
      id: article.id,
      date: article.created_at,
      title: article.title
    });
    yearData.count++;
  });
  
  // 转换为数组并按年份倒序排序
  return Array.from(yearMap.values())
    .sort((a, b) => Number(b.id) - Number(a.id))
    .filter(category => category.count > 0);
});

// 当前显示的分类数据
const categories = computed(() =>
  categoryType.value === 'tag' ? tagCategories.value : yearCategories.value
);

// 跳转到文章详情页
const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`);
};
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
