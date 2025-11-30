<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-bold mb-4">热门文章</h3>
    <ul class="space-y-3">
      <li 
        v-for="article in hotArticles" 
        :key="article.id" 
        class="text-gray-600 hover:text-blue-600 cursor-pointer truncate"
        @click="handleArticleClick(article.id)"
      >
        {{ article.title }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

// 定义props
interface Props {
  hotArticles: Array<{
    id: number;
    title: string;
  }>;
  onArticleClick?: (articleId: number) => void;
}

const props = defineProps<Props>();

// 文章点击处理
const handleArticleClick = (articleId: number) => {
  // 如果父组件提供了自定义点击处理，则使用它
  if (props.onArticleClick) {
    props.onArticleClick(articleId);
  } else {
    // 否则默认跳转到文章详情页
    router.push(`/article/${articleId}`);
  }
};
</script>
