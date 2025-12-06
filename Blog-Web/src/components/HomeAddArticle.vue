<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-bold mb-4 text-stone-800">添加内容</h3>
    <div class="flex gap-3">
      <el-button 
        type="primary" 
        plain
        size="large" 
        @click="goToPublish"
        class="flex-1 bg-stone-800 hover:bg-stone-700 border-stone-800"
      >
        <el-icon class="mr-2">
          <EditPen />
        </el-icon>
        新建文章
      </el-button>
      <el-button 
        type="primary" 
        plain
        size="large" 
        @click="goToAddProgram"
        class="flex-1 bg-blue-600 hover:bg-blue-500 border-blue-600"
      >
        <el-icon class="mr-2">
          <FolderAdd />
        </el-icon>
        新建项目
      </el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { EditPen, FolderAdd } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 跳转到发布页面
const goToPublish = () => {
  router.push('/addarticle');
};

// 跳转到新增项目页面
const goToAddProgram = () => {
  router.push('/addprogram');
};
</script>
