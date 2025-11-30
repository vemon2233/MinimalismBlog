<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-bold mb-4">文章归档</h3>
    <ul class="space-y-2">
      <li 
        v-for="archive in archives" 
        :key="archive.date" 
        :class="[
          'flex justify-between items-center cursor-pointer transition-colors',
          selectedArchive === archive.date 
            ? 'text-blue-600 font-medium' 
            : 'text-gray-600 hover:text-blue-600'
        ]"
        @click="handleArchiveClick(archive.date)"
      >
        <span>{{ archive.date }}</span>
        <span class="text-gray-400">({{ archive.count }})</span>
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
// 定义props
interface Props {
  archives: Array<{
    date: string;
    count: number;
  }>;
  selectedArchive?: string;
  onArchiveClick?: (date: string) => void;
}

const props = defineProps<Props>();

// 归档点击处理
const handleArchiveClick = (date: string) => {
  if (props.onArchiveClick) {
    props.onArchiveClick(date);
  }
};
</script>
