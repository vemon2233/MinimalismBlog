<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-bold mb-4">标签云</h3>
    <div class="flex flex-wrap gap-2">
      <el-tag 
        v-for="tag in allTags" 
        :key="tag" 
        :class="['cursor-pointer !rounded-button', selectedTag === tag ? 'bg-blue-100' : '']" 
        @click="handleTagClick(tag)"
      >
        {{ tag }}
      </el-tag>
    </div>
  </div>
</template>

<script lang="ts" setup>
// 定义props
interface Props {
  allTags: string[];
  selectedTag: string;
  onTagClick?: (tag: string) => void;
}

const props = defineProps<Props>();

// 标签点击处理
const handleTagClick = (tag: string) => {
  if (props.onTagClick) {
    props.onTagClick(tag);
  }
};
</script>
