<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-xl font-bold text-gray-900 mb-6">评论区</h3>
    
    <!-- 评论表单 -->
    <div class="mb-6">
      <el-input v-model="authorName" placeholder="昵称（选填，最多8个字）" class="mb-4" maxlength="8" show-word-limit />
      <el-input v-model="authorEmail" placeholder="邮箱（选填）" class="mb-4" />
      <el-input v-model="commentContent" type="textarea" :rows="4" placeholder="写下你的评论（最多100个字）..." class="mb-4"
        maxlength="100" show-word-limit />
      <el-button type="primary" class="!rounded-button" @click="submitComment" :loading="submitting">
        发表评论
      </el-button>
    </div>
    
    <!-- 评论列表 -->
    <div v-if="loading" class="text-center py-8">
      <el-icon class="text-2xl text-gray-400 animate-spin"><Loading /></el-icon>
      <p class="mt-2 text-gray-600">加载评论中...</p>
    </div>
    
    <div v-else-if="comments.length > 0" class="space-y-6">
      <div v-for="comment in comments" :key="comment.id" class="bg-gray-50 rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center">
            <el-icon>
              <User />
            </el-icon>
            <span class="ml-2 font-medium text-gray-700">{{ comment.author_name || '匿名用户' }}</span>
          </div>
          <span class="text-sm text-gray-500">{{ formatTime(comment.created_at) }}</span>
        </div>
        <p class="text-gray-700">{{ comment.content }}</p>
      </div>
    </div>
    
    <div v-else class="text-center py-8 text-gray-500">
      暂无评论，快来发表第一条评论吧！
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { User, Loading } from '@element-plus/icons-vue';
import { articleService } from '../services/api';

// Props
const props = defineProps<{
  articleId: number
}>();

// 响应式数据
const authorName = ref('');
const authorEmail = ref('');
const commentContent = ref('');
const comments = ref([]);
const loading = ref(false);
const submitting = ref(false);

// 格式化时间显示
const formatTime = (timeString: string) => {
  const now = new Date();
  
  // 处理后端返回的时间字符串，确保正确解析
  let commentTime;
  if (timeString.includes('T')) {
    // ISO 8601 格式
    commentTime = new Date(timeString);
  } else {
    // 自定义格式 'YYYY-MM-DD HH:MM:SS'
    commentTime = new Date(timeString.replace(' ', 'T') + 'Z');
  }
  
  // 计算时间差（毫秒）
  const diff = now.getTime() - commentTime.getTime();
  
  if (diff < 60000) return '刚刚';
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`;
  if (diff < 2592000000) return `${Math.floor(diff / 86400000)} 天前`;
  
  return commentTime.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

// 加载评论
const loadComments = async () => {
  loading.value = true;
  try {
    const response = await articleService.getComments(props.articleId);
    comments.value = response.comments || [];
  } catch (error) {
    console.error('加载评论失败:', error);
    ElMessage.error('加载评论失败');
  } finally {
    loading.value = false;
  }
};

// 提交评论
const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容');
    return;
  }

  // 检查昵称长度
  if (authorName.value && authorName.value.length > 8) {
    ElMessage.warning('昵称最多输入8个字');
    return;
  }

  // 检查评论长度
  if (commentContent.value.length > 100) {
    ElMessage.warning('评论最多输入100个字');
    return;
  }

  submitting.value = true;
  try {
    await articleService.createComment(props.articleId, {
      author_name: authorName.value || '匿名用户',
      author_email: authorEmail.value,
      content: commentContent.value
    });
    
    ElMessage.success('评论发表成功');
    
    // 清空表单
    commentContent.value = '';
    authorName.value = '';
    authorEmail.value = '';
    
    // 重新加载评论列表
    await loadComments();
    
  } catch (error) {
    console.error('发表评论失败:', error);
    ElMessage.error('发表评论失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
};

// 组件挂载时加载评论
onMounted(() => {
  loadComments();
});
</script>

<style scoped>
.el-input :deep(.el-input__wrapper) {
  background-color: #f9fafb;
  border: none;
  box-shadow: none;
}

.el-textarea :deep(.el-textarea__inner) {
  background-color: #f9fafb;
  border: none;
  box-shadow: none;
}
</style>
