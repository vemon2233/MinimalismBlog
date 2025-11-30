<template>
  <nav class="fixed top-0 w-full bg-white shadow-sm z-50">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <h1 class="text-2xl font-bold text-gray-800">
          <a href="/" class="text-gray-800 hover:text-gray-900">极简主义博客</a>
        </h1>
      </div>
      <div class="flex items-center space-x-6">
        <div class="relative">
          <ElInput v-model="searchText" placeholder="搜索文章..." class="w-64" :prefix-icon="Search"
            @keyup.enter="handleSearch" />
        </div>
        <nav class="hidden md:flex items-center space-x-6">
          <a v-for="item in navItems" :key="item.name" :href="item.url" :class="[
            'whitespace-nowrap',
            $route.path === item.url ? 'text-blue-600 hover:text-blue-600' : 'hover:text-gray-500'
            ]">
            {{ item.name }}
          </a>
        </nav>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Search } from '@element-plus/icons-vue';
import { ElInput } from 'element-plus';

const router = useRouter();

// 导航项直接包含链接地址
const navItems = [
  { name: '首页', url: '/home' },
  { name: '归档', url: '/listing' },
  { name: '项目', url: '/program' },
  { name: '简历', url: '/resume' }
];

const searchText = ref('');

// 处理搜索提交
const handleSearch = () => {
  if (searchText.value.trim()) {
    // 使用Vue Router跳转到搜索结果页
    router.push({
      path: '/search',
      query: {
        q: searchText.value.trim()
      }
    });
  }
};
</script>

<style scoped>
.el-input :deep(.el-input__wrapper) {
  background-color: #f9fafb;
  border: none;
  box-shadow: none;
}

.el-input :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #e5e7eb;
  border-radius: 0.375rem;
}

.el-input :deep(.el-input__wrapper):hover {
  box-shadow: 0 0 0 1px #d1d5db;
}

.el-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}
</style>
