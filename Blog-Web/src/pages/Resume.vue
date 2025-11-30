<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
    <!-- 个人信息区域 -->
    <header class="pt-20 pb-16">
      <div class="container mx-auto px-4 py-8 max-w-7xl flex gap-8">
        <!-- 左侧个人信息 -->
        <div class="w-1/4 top-8">
          <ResumeProfileCard />
        </div>

        <!-- 右侧个人经历 -->
        <div class="w-3/4 space-y-6">
          <ResumeWorkExperience />
        </div>
      </div>
    </header>

    <!-- 作品展示区域 -->
    <section class="pb-20">
      <div class="container mx-auto px-4 max-w-7xl">
        <!-- 标题 -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">个人作品</h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">
            以下是我在技术生涯中开发的一些代表性项目，涵盖了前端、后端和全栈开发
          </p>
        </div>

        <!-- 作品网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <ResumeProduct 
            v-for="product in products" 
            :key="product.id" 
            :product="product" 
          />
        </div>
      </div>
    </section>

    <!-- 返回顶部按钮 -->
    <el-backtop :right="40" :bottom="40" />
  </div>
</template>

<route>
{
  meta: {
    title: "个人简历 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref } from 'vue';
import ResumeProfileCard from '../components/ResumeProfileCard.vue';
import ResumeWorkExperience from '../components/ResumeWorkExperience.vue';
import ResumeProduct from '../components/ResumeProduct.vue';

// 模拟作品数据
const products = ref([
  {
    id: 1,
    title: '智能博客管理系统',
    description: '基于Vue 3 + Element Plus + Flask的全栈博客系统，支持文章管理、标签分类、用户评论等功能。',
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop',
    tags: ['Vue 3', 'Flask', 'MySQL'],
    features: ['响应式设计', 'RESTful API', 'Markdown支持'],
    demoUrl: 'https://demo.example.com',
    githubUrl: 'https://github.com/example/blog-system'
  },
  {
    id: 2,
    title: '企业级数据可视化平台',
    description: '为企业提供数据分析和可视化展示的平台，支持多种图表类型和实时数据更新。',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop',
    tags: ['React', 'D3.js', 'Node.js'],
    features: ['实时数据', '多种图表', '权限管理'],
    demoUrl: 'https://demo.example.com/dashboard',
    githubUrl: 'https://github.com/example/data-visualization'
  },
  {
    id: 3,
    title: '微服务架构电商系统',
    description: '采用微服务架构的电商平台，包含用户服务、商品服务、订单服务和支付服务等模块。',
    image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop',
    tags: ['Spring Boot', 'Docker', 'Redis'],
    features: ['微服务', '容器化', '高可用'],
    demoUrl: 'https://shop.example.com',
    githubUrl: 'https://github.com/example/ecommerce'
  },
  {
    id: 4,
    title: 'AI智能写作助手',
    description: '基于深度学习的智能写作工具，支持文章生成、语法检查、内容优化等功能。',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
    tags: ['Python', 'TensorFlow', 'FastAPI'],
    features: ['AI生成', '语法检查', '内容优化'],
    demoUrl: 'https://ai-writer.example.com',
    githubUrl: 'https://github.com/example/ai-writer'
  }
]);
</script>

<style scoped></style>
