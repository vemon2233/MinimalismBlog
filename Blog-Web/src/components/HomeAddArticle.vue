<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-bold mb-4 text-stone-800">添加文章</h3>
    <el-button 
      type="primary" 
      size="large" 
      @click="goToPublish"
      class="w-full bg-stone-800 hover:bg-stone-700 border-stone-800"
    >
      <el-icon class="mr-2">
        <Plus />
      </el-icon>
      写文章
    </el-button>
  </div>
</template>

<script lang="ts" setup>
import { Plus } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 跳转到发布页面
const goToPublish = () => {
  router.push('/publish');
};
</script>
