<template>
  <!-- 项目展示区域 -->
  <main class="max-w-7xl mx-auto px-4 pb-20">
    <div class="grid grid-cols-3 gap-8">
      <div v-for="project in projects" :key="project.id"
        class="project-card bg-white rounded-xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer"
        @click="navigateToProject(project.id)">
        <img :src="project.image" :alt="project.title" class="w-full h-48 object-cover rounded-lg mb-6" />
        <h3 class="text-xl font-semibold mb-3 text-gray-800">{{ project.title }}</h3>
        <p class="text-gray-600">{{ project.description }}</p>
      </div>
    </div>
  </main>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

const projects = ref([
  {
    id: 1,
    title: '企业级 SaaS 管理平台',
    description: '基于 Vue3 + TypeScript 的现代化企业管理系统，包含数据可视化、权限管理等核心功能',
    image: 'https://ai-public.mastergo.com/ai/img_res/1b812a61dec113830d25435ac25f027b.jpg'
  },
  {
    id: 2,
    title: '电商移动端应用',
    description: '基于 React Native 开发的跨平台电商应用，支持商品浏览、购物车、支付等功能',
    image: 'https://ai-public.mastergo.com/ai/img_res/912a02d2886c7b2d77540214e7025889.jpg'
  },
  {
    id: 3,
    title: '智能家居控制系统',
    description: '物联网智能家居控制平台，支持多设备联动、场景管理、数据统计等功能',
    image: 'https://ai-public.mastergo.com/ai/img_res/99421ad5b6cd9ddc762799cd25ed5fae.jpg'
  },
  {
    id: 4,
    title: '在线教育平台',
    description: '集成视频直播、课程管理、作业系统的综合性在线教育解决方案',
    image: 'https://ai-public.mastergo.com/ai/img_res/d2935384de4d5be65738829449a8d54c.jpg'
  },
  {
    id: 5,
    title: '数据可视化大屏',
    description: '基于 ECharts 的企业数据可视化解决方案，支持多维度数据展示和实时更新',
    image: 'https://ai-public.mastergo.com/ai/img_res/032112d176f6fd43ede6cf21f1fde427.jpg'
  },
  {
    id: 6,
    title: '企业官网重构项目',
    description: '使用 Next.js 重构的企业官网，优化了性能和SEO，提升用户体验',
    image: 'https://ai-public.mastergo.com/ai/img_res/6d62090f967d0d8093dd6386c76810c2.jpg'
  }
]);
const navigateToProject = (projectId: number) => {
  // 在实际应用中替换为真实的项目详情页面路由
  console.log(`Navigate to project ${projectId}`);
};
</script>

<style scoped>
.project-card:hover {
  transform: translateY(-4px);
}
</style>