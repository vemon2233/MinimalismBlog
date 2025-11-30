<template>
  <div class="bg-white rounded-lg shadow-sm p-6 transform transition-all duration-300 hover:shadow-md">
    <!-- 作品图片 -->
    <div class="relative mb-4">
      <img 
        :src="product.image" 
        :alt="product.title" 
        class="w-full h-48 object-cover rounded-lg"
      />
      <!-- 技术标签 -->
      <div class="absolute top-3 right-3 flex flex-wrap gap-1">
        <span 
          v-for="tag in product.tags" 
          :key="tag"
          class="px-2 py-1 bg-black/70 text-white text-xs rounded-full"
        >
          {{ tag }}
        </span>
      </div>
    </div>

    <!-- 作品信息 -->
    <div class="space-y-3">
      <!-- 标题和描述 -->
      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ product.title }}</h3>
        <p class="text-gray-600 text-sm leading-relaxed">{{ product.description }}</p>
      </div>

      <!-- 项目链接 -->
      <div class="flex gap-2">
        <el-button 
          v-if="product.demoUrl"
          size="small" 
          type="primary" 
          class="!rounded-button"
          @click="openLink(product.demoUrl)"
        >
          <el-icon class="mr-1">
            <View />
          </el-icon>
          在线演示
        </el-button>
        <el-button 
          v-if="product.githubUrl"
          size="small" 
          class="!rounded-button"
          @click="openLink(product.githubUrl)"
        >
          <el-icon class="mr-1">
            <Star />
          </el-icon>
          GitHub
        </el-button>
      </div>

      <!-- 项目特色 -->
      <div class="flex flex-wrap gap-1">
        <span 
          v-for="feature in product.features" 
          :key="feature"
          class="px-2 py-1 bg-blue-50 text-blue-600 text-xs rounded-full"
        >
          {{ feature }}
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { View, Star } from '@element-plus/icons-vue';

interface Product {
  id: number;
  title: string;
  description: string;
  image: string;
  tags: string[];
  features: string[];
  demoUrl?: string;
  githubUrl?: string;
}

defineProps<{
  product: Product;
}>();

// 打开链接
const openLink = (url: string) => {
  window.open(url, '_blank');
};
</script>

<style scoped>
/* 悬停效果 */
.transform {
  transition: all 0.3s ease;
}

.hover\:shadow-md:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>
