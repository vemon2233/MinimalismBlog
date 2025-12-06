<template>
  <article class="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
    <h2 class="text-xl font-bold mb-2 hover:text-stone-600 transition-colors cursor-pointer" @click="handleArticleClick">
      {{ article.title }}
      <span v-if="showProgramName && article.program_name" class="text-sm font-normal text-blue-600 ml-2">
        [{{ article.program_name }}]
      </span>
    </h2>

    <!-- 文章元信息 -->
    <div class="flex items-center text-sm text-gray-500 mb-3 space-x-4">
      <span class="flex items-center">
        <el-icon class="mr-1">
          <Calendar />
        </el-icon>
        {{ article.created_at }}
      </span>
      <span class="flex items-center">
        <el-icon class="mr-1">
          <Timer />
        </el-icon>
        {{ formatReadTime(article.read_time) }}
      </span>
      <span class="flex items-center">
        <el-icon class="mr-1">
          <View />
        </el-icon>
        {{ article.view_count || 0 }}
      </span>
      <span class="flex items-center">
        <el-icon class="mr-1">
          <Star />
        </el-icon>
        {{ article.like_count || 0 }}
      </span>
      <span class="flex items-center">
        <el-icon class="mr-1">
          <ChatDotRound />
        </el-icon>
        {{ article.comment_count || 0 }}
      </span>
    </div>

    <!-- 文章摘要 -->
    <p class="text-gray-600 mb-4 line-clamp-3">{{ article.excerpt }}</p>

    <!-- 标签 -->
    <div class="flex flex-wrap gap-2">
      <el-tag v-for="tag in article.tags" :key="tag" class="!rounded-button cursor-pointer"
        @click.stop="handleTagClick(tag)">
        {{ tag }}
      </el-tag>
    </div>
  </article>
</template>

<script lang="ts" setup>
import { Calendar, Timer, View, Star, ChatDotRound } from '@element-plus/icons-vue';

// 定义props
interface Props {
  article: {
    id: number;
    title: string;
    created_at: string;
    read_time: number;
    view_count: number;
    like_count: number;
    comment_count: number;
    excerpt: string;
    tags: string[];
    program_name?: string;
  };
  onTagClick?: (tag: string) => void;
  showProgramName?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  onTagClick: undefined,
  showProgramName: false
});

// 定义emits
const emit = defineEmits<{
  'article-click': [id: number];
  'tag-click': [tag: string];
}>();

// 格式化阅读时间
const formatReadTime = (minutes: number) => {
  if (minutes < 60) {
    return `${minutes} 分钟阅读`;
  } else {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    if (remainingMinutes === 0) {
      return `${hours} 小时阅读`;
    } else {
      return `${hours} 小时 ${remainingMinutes} 分钟阅读`;
    }
  }
};

// 处理文章点击
const handleArticleClick = () => {
  emit('article-click', props.article.id);
};

// 处理标签点击
const handleTagClick = (tag: string) => {
  if (props.onTagClick) {
    props.onTagClick(tag);
  } else {
    emit('tag-click', tag);
  }
};
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
