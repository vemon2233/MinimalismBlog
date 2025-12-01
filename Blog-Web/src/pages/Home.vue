<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 pt-24 pb-12">
      <div class="flex flex-col md:flex-row gap-8">
        <!-- 左侧文章列表 -->
        <main class="flex-1">
          <!-- 错误状态 -->
          <ApiErrorState 
            v-if="apiError" 
            @retry="loadData" 
          />
          
          <!-- 数据加载完成后的状态 -->
          <div v-else-if="dataLoaded">
            <!-- 服务正常但无文章 -->
            <div v-if="filteredPosts.length === 0" class="bg-white rounded-lg shadow-sm p-8 text-center">
              <el-icon class="text-gray-400 text-4xl mb-4">
                <Document />
              </el-icon>
              <h3 class="text-xl font-bold text-gray-800 mb-2">暂无文章</h3>
              <p class="text-gray-600">当前筛选条件下没有找到相关文章</p>
            </div>
            
            <!-- 正常状态：有文章 -->
            <div v-else class="space-y-6">
              <SingleArticle 
                v-for="post in filteredPosts" 
                :key="post.id"
                :article="post"
                @article-click="goToArticle"
                @tag-click="filterByTag"
              />
              
              <!-- 分页 -->
              <div class="mt-8 flex justify-center">
                <el-pagination v-model:current-page="currentPage" :page-size="5" :total="totalArticles"
                  layout="prev, pager, next" @current-change="handlePageChange" />
              </div>
            </div>
          </div>
          
          <!-- 数据加载中：显示空白 -->
          <div v-else>
            <!-- 数据加载完成前显示空白 -->
          </div>
        </main>
        <!-- 右侧边栏 -->
        <aside class="w-80 space-y-6">
          <!-- 添加文章组件 -->
          <HomeAddArticle 
            :all-tags="allTags" 
            @article-added="loadData" 
          />
          
          <!-- 标签云组件 -->
          <HomeTagCloud 
            :all-tags="allTags" 
            :selected-tag="selectedTag" 
            @tag-click="filterByTag" 
          />
          
          <!-- 热门文章组件 -->
          <HomeHotArticles 
            :hot-articles="hotArticles" 
            @article-click="handleArticleClick" 
          />
          
          <!-- 归档组件 -->
          <HomeArticleArchive 
            :archives="archives" 
            :selected-archive="selectedArchive"
            @archive-click="handleArchiveClick" 
          />
        </aside>
      </div>
    </div>
    <!-- 回到顶部 -->
    <el-backtop :right="20" :bottom="20" />
  </div>
</template>

<route>
{
  meta: {
    title: "首页 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Calendar, Timer, View, Star, ChatDotRound, Document } from '@element-plus/icons-vue';
import { articleService, otherService } from '../apis';
import SingleArticle from '../components/SingleArticle.vue';
import ApiErrorState from '../components/ApiErrorState.vue';

const router = useRouter();

const searchText = ref('');
const currentPage = ref(1);
const selectedTag = ref('');
const selectedArchive = ref('');
const posts = ref([]);
const allTags = ref([]);
const hotArticles = ref([]);
const archives = ref([]);
const totalArticles = ref(0);
const apiError = ref(false);
const dataLoaded = ref(false); // 标记数据是否已加载完成

// 加载数据
const loadData = async () => {
  apiError.value = false; // 重置错误状态
  dataLoaded.value = false; // 重置数据加载状态
  try {
    // 并行加载所有数据
    const [articlesResponse, tagsResponse, hotResponse, archivesResponse] = await Promise.all([
      articleService.getArticles({
        page: currentPage.value,
        per_page: 5,
        tag: selectedTag.value || undefined,
        archive: selectedArchive.value || undefined
      }),
      otherService.getTags(),
      articleService.getHotArticles(),
      articleService.getArchives()
    ]);

    // 设置数据
    posts.value = articlesResponse.articles;
    totalArticles.value = articlesResponse.total;
    // 从tagsResponse.tags中提取标签名称（现在tags是对象数组，包含name和count）
    allTags.value = tagsResponse.tags.map(tag => tag.name);
    hotArticles.value = hotResponse.hot_articles;
    archives.value = archivesResponse.archives;

    // 标记数据加载完成
    dataLoaded.value = true;

  } catch (error) {
    console.error('加载数据失败:', error);
    // 如果API调用失败，设置错误状态
    apiError.value = true;
    posts.value = [];
    allTags.value = [];
    hotArticles.value = [];
    archives.value = [];
    totalArticles.value = 0;
    // 即使出错也标记为已加载，以便显示错误状态
    dataLoaded.value = true;
  }
};

// 页面加载时获取数据
onMounted(() => {
  loadData();
});

// 页码变化时重新加载数据
const handlePageChange = () => {
  loadData();
};

// 标签筛选
const filterByTag = (tag: string) => {
  selectedTag.value = selectedTag.value === tag ? '' : tag;
  currentPage.value = 1;
  loadData();
};

const filteredPosts = computed(() => {
  let result = [...posts.value];
  if (searchText.value) {
    result = result.filter(post =>
      post.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(searchText.value.toLowerCase())
    );
  }
  if (selectedTag.value) {
    result = result.filter(post => post.tags.includes(selectedTag.value));
  }
  return result;
});

// 热门文章点击处理
const handleArticleClick = (articleId: number) => {
  // 跳转到文章详情页
  router.push(`/article/${articleId}`);
};

// 归档点击处理
const handleArchiveClick = (date: string) => {
  selectedArchive.value = selectedArchive.value === date ? '' : date;
  currentPage.value = 1;
  loadData();
};

// 跳转到文章详情页
const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`);
};
</script>

<style scoped>
.el-pagination :deep(.el-pager li.is-active) {
  background-color: #3b82f6;
  color: white;
}

.el-pagination :deep(.el-pager li:hover) {
  color: #3b82f6;
}
</style>
