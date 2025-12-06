<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto px-4 pt-30 pb-12">
      <!-- 错误状态 -->
      <ApiErrorState v-if="apiError" @retry="loadProjects" />

      <!-- 数据加载完成后的状态 -->
      <div v-else-if="dataLoaded">
        <!-- 项目展示区域 -->
        <div class="max-w-7xl mx-auto px-4 pb-20">
          <!-- 服务正常但无项目 -->
          <div v-if="totalProjects === 0" class="bg-white rounded-lg shadow-sm p-8 text-center">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <h3 class="text-xl font-bold text-gray-800 mb-2">暂无项目</h3>
            <p class="text-gray-600">当前没有可展示的项目</p>
          </div>

          <!-- 正常状态：有项目 -->
          <div v-else>
            <div class="grid grid-cols-3 gap-8">
              <!-- 真实项目卡片 -->
              <div v-for="project in displayedProjects" :key="project.id"
                class="project-card bg-white rounded-xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer h-[420px] flex flex-col"
                @click="navigateToProject(project.id)">
                <img :src="project.image_url || 'http://localhost:5173/static/uploads/projects/not_found.png'"
                  :alt="project.name" class="w-full h-48 object-fill rounded-lg mb-6 flex-shrink-0" />
                <h3 class="text-xl font-semibold mb-3 text-gray-800 flex-shrink-0">{{ project.name }}</h3>
                <p class="text-gray-600 flex-1 overflow-hidden line-clamp-4">{{ project.description }}</p>
              </div>

              <!-- 开发中占位卡片 -->
              <div v-for="index in placeholderCount" :key="`placeholder-${index}`"
                class="bg-white rounded-xl p-8 shadow-sm h-[420px] flex flex-col">
                <img src="http://localhost:5173/static/uploads/projects/developing.png" alt="开发中项目"
                  class="w-full h-48 object-cover rounded-lg mb-6 opacity-50 flex-shrink-0" />
                <h3 class="text-xl font-semibold mb-3 text-gray-400 flex-shrink-0">项目开发中</h3>
                <p class="text-gray-400 flex-1 flex justify-center">新项目正在紧张开发中，敬请期待更多精彩内容...</p>
              </div>
            </div>

            <!-- 分页控件 -->
            <div v-if="totalPages > 1" class="mt-8 flex justify-center">
              <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="totalProjects"
                layout="prev, pager, next" />
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
</template>

<route>
{
  meta: {
    title: "项目管理 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Plus } from '@element-plus/icons-vue';
import ApiErrorState from '../components/ApiErrorState.vue';
import programService from '../apis/program.js';

const router = useRouter();

// 响应式数据
const apiError = ref(false);
const dataLoaded = ref(false); // 标记数据是否已加载完成
const projects = ref([]);
const currentPage = ref(1);
const pageSize = 6; // 每页显示6个项目

// 计算属性
const totalProjects = computed(() => projects.value.length);
const totalPages = computed(() => Math.ceil(totalProjects.value / pageSize));
const startIndex = computed(() => (currentPage.value - 1) * pageSize);
const endIndex = computed(() => startIndex.value + pageSize);
const displayedProjects = computed(() => projects.value.slice(startIndex.value, endIndex.value));
const placeholderCount = computed(() => {
  const displayedCount = displayedProjects.value.length;
  return Math.max(0, pageSize - displayedCount);
});

const navigateToCreate = () => {
  router.push('/addprogram');
};

const navigateToProject = (projectId: number) => {
  router.push(`/program/${projectId}`);
};

const loadProjects = async () => {
  apiError.value = false;
  dataLoaded.value = false;
  
  try {
    const response = await programService.getAllProjects();
    // 检查响应数据结构 - 根据API测试，应该是response.data.projects
    if (response && response.projects) {
      projects.value = response.projects;
    } else {
      projects.value = [];
    }
    dataLoaded.value = true;
  } catch (error) {
    console.error('加载项目失败:', error);
    apiError.value = true;
    dataLoaded.value = true; // 即使出错也标记为已加载，以便显示错误状态
  }
};

onMounted(() => {
  loadProjects();
});
</script>

<style scoped>
.project-card:hover {
  transform: translateY(-4px);
}
</style>
