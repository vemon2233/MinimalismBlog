<template>
  <div v-for="(experience, index) in workExperiences" :key="index"
    class="bg-white rounded-lg shadow-sm p-6 transform transition-all duration-300 hover:shadow-md">
    <div class="flex items-start gap-4">
      <div class="bg-blue-50 rounded-lg p-3">
        <el-icon class="text-3xl text-blue-500">
          <component :is="experience.icon" />
        </el-icon>
      </div>
      <div class="flex-1">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-xl font-semibold">{{ experience.company }}</h3>
          <span class="text-gray-500 text-sm whitespace-nowrap">{{ experience.period }}</span>
        </div>
        <div class="text-gray-700 font-medium mb-2">{{ experience.position }}</div>
        <div class="space-y-2">
          <div v-for="(achievement, idx) in experience.achievements" :key="idx"
            class="text-gray-600 flex items-start gap-2">
            <div class="w-1 h-1 rounded-full bg-gray-400 mt-2 flex-shrink-0"></div>
            <p>{{ achievement }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
const workExperiences = [
  {
    company: '字节跳动',
    position: '高级前端工程师',
    period: '2023 - 至今',
    icon: 'Monitor',
    achievements: [
      '负责抖音企业版核心功能开发，带领团队完成直播数据分析平台的架构设计和实现，提升数据处理效率 300%',
      '优化前端构建流程，将构建时间从 15 分钟降低到 3 分钟，大幅提升团队开发效率',
      '设计并实现组件库，提供超过 50 个高复用性组件，覆盖率达到 90%'
    ]
  },
  {
    company: '腾讯科技',
    position: '前端工程师',
    period: '2021 - 2023',
    icon: 'TrendCharts',
    achievements: [
      '参与微信小程序开发者工具的功能优化，实现了实时预览和调试功能，月活用户增长 50%',
      '主导开发团队管理系统，集成 Jenkins 自动化部署，将发布流程从 4 小时缩短至 30 分钟',
      '重构legacy代码，将代码覆盖率提升至 85%，显著提升了系统稳定性'
    ]
  }
];
</script>

<style scoped></style>