<template>
  <div class="bg-white rounded-lg shadow-sm p-8 text-center">
    <el-icon class="text-red-500 text-4xl mb-4">
      <Warning />
    </el-icon>
    <h3 class="text-xl font-bold text-gray-800 mb-2">{{ title }}</h3>
    <p class="text-gray-600 mb-4">{{ message }}</p>
    <el-button v-if="showRetry" type="primary" @click="handleRetry">
      <el-icon class="mr-1">
        <Refresh />
      </el-icon>
      {{ retryText }}
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { Warning, Refresh } from '@element-plus/icons-vue';

// 定义props
interface Props {
  title?: string;
  message?: string;
  showRetry?: boolean;
  retryText?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: '服务异常',
  message: '无法连接到服务器，请检查网络连接或稍后重试',
  showRetry: true,
  retryText: '重新加载'
});

// 定义emits
const emit = defineEmits<{
  'retry': [];
}>();

// 处理重试
const handleRetry = () => {
  emit('retry');
};
</script>

<style scoped>
/* 组件样式 */
</style>
