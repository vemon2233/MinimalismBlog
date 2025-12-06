<template>
  <!-- 编辑模式且没有评论时，不显示整个组件 -->
  <div v-if="!isEditing || comments.length > 0" class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-xl font-bold text-gray-900 mb-6">评论区</h3>
    
    <!-- 评论表单（编辑模式下隐藏） -->
    <div v-if="!isEditing" class="mb-6">
      <el-input v-model="authorName" placeholder="昵称（选填，最多8个字）" class="mb-4" maxlength="8" show-word-limit />
      <el-input v-model="authorEmail" placeholder="邮箱（选填）" class="mb-4" />
      <el-input v-model="commentContent" type="textarea" :rows="4" placeholder="写下你的评论（最多100个字）..." class="mb-4"
        maxlength="100" show-word-limit />
      <div class="flex justify-end">
        <el-button type="primary" plain class="!rounded-button" @click="submitComment" :loading="submitting">
          发表评论
        </el-button>
      </div>
    </div>
    
    <!-- 评论列表 -->
    <div v-if="loading">
    </div>
    
    <div v-else-if="pagedComments.length > 0" class="space-y-6">
      <div v-for="comment in pagedComments" :key="comment.id" class="bg-gray-50 rounded-lg p-4 relative">
        <!-- 编辑模式下的删除按钮 -->
        <div v-if="isEditing" class="absolute top-2 right-2 z-10">
          <el-button type="danger" link @click.stop="deleteComment(comment.id)">
            删除
          </el-button>
        </div>
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center">
            <el-icon>
              <User />
            </el-icon>
            <span class="ml-2 font-medium text-gray-700">{{ comment.author_name || '匿名用户' }}</span>
          </div>
        </div>
        <p class="text-gray-700">{{ comment.content }}</p>
        <span class="text-sm text-gray-500">{{ formatTime(comment.created_at) }}</span>
      </div>
      
      <!-- 分页组件 -->
      <div v-if="comments.length > pageSize" class="mt-8 flex justify-center">
        <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="comments.length"
          layout="prev, pager, next" @current-change="handlePageChange" />
      </div>
    </div>
    
    <div v-else-if="!isEditing" class="text-center py-8 text-gray-500">
      暂无评论，快来发表第一条评论吧！
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { User } from '@element-plus/icons-vue';
import { commentService } from '../apis';

// Props
const props = defineProps<{
  articleId: number,
  isEditing?: boolean
}>();

// 响应式数据
const authorName = ref('');
const authorEmail = ref('');
const commentContent = ref('');
const comments = ref([]);
const loading = ref(false);
const submitting = ref(false);

// 分页相关
const currentPage = ref(1);
const pageSize = ref(5); // 每页显示5条评论

// 计算当前页的评论
const pagedComments = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return comments.value.slice(start, end);
});

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
    const response = await commentService.getComments(props.articleId);
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
    await commentService.createComment(props.articleId, {
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

// 删除评论
const deleteComment = async (commentId: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条评论吗？此操作不可撤销。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await commentService.deleteComment(commentId);
    
    ElMessage.success('评论删除成功！');
    
    // 从本地数据中移除这条评论
    comments.value = comments.value.filter(comment => comment.id !== commentId);
    
    // 如果删除后当前页没有评论了，且不是第一页，则跳转到前一页
    if (pagedComments.value.length === 0 && currentPage.value > 1) {
      currentPage.value = currentPage.value - 1;
    }
    
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error);
      ElMessage.error(error.response?.data?.error || '删除评论失败，请重试');
    }
  }
};

// 分页变化处理
const handlePageChange = () => {
  // 滚动到评论区域顶部
  const commentSection = document.querySelector('.bg-white.rounded-lg.shadow-sm');
  if (commentSection) {
    commentSection.scrollIntoView({ behavior: 'smooth' });
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
