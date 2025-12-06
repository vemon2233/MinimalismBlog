<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 文章内容区 -->
    <main class="max-w-7xl mx-auto px-4 pt-30 pb-12">
      <!-- 数据加载完成后的状态 -->
      <div v-if="dataLoaded">
        <div v-if="article">
          <!-- 编辑模式 -->
          <div v-if="isEditing" class="bg-white rounded-lg shadow-sm p-6 mb-8">
            <div class="flex justify-between items-center mb-6">
              <h1 class="text-2xl font-bold text-gray-800">编辑文章</h1>
              <div class="flex gap-2">
                <el-button type="success" plain :icon="Check" @click="handleSaveEdit" :loading="editLoading">
                  保存
                </el-button>
                <el-button :icon="Close" @click="cancelEdit">
                  取消
                </el-button>
              </div>
            </div>
            <!-- 使用EditArticle组件 -->
            <EditArticle
              ref="editArticleRef"
              :initial-data="editForm"
              :submitting="editLoading"
              @update:submitting="editLoading = $event"
              @submit="handleUpdateArticle"
            />
          </div>

          <!-- 查看模式 -->
          <div v-else>
            <article class="bg-white rounded-lg shadow-sm p-6 mb-8">
              <div class="flex justify-between items-start mb-4">
                <h1 class="text-3xl font-bold text-gray-900">{{ article.title }}</h1>
                <div class="flex gap-2">
                  <el-button type="primary" plain :icon="Edit" @click="startEdit">
                    编辑
                  </el-button>
                  <el-button type="danger" plain :icon="Delete" @click="handleDelete">
                    删除
                  </el-button>
                </div>
              </div>
              <div class="flex items-center text-gray-500 text-sm mb-8 space-x-6">
                <!-- 显示项目名称 -->
                <span v-if="article.program_name" class="flex items-center">
                  <el-icon>
                    <Folder />
                  </el-icon>
                  <span class="ml-2 text-blue-600 hover:text-blue-800 cursor-pointer transition-colors"
                    @click="goToProgram">
                    {{ article.program_name }}
                  </span>
                </span>

                <span class="flex items-center">
                  <el-icon>
                    <Calendar />
                  </el-icon>
                  <span class="ml-2">{{ formatDate(article.created_at) }}</span>
                </span>
                <span class="flex items-center">
                  <el-icon>
                    <Timer />
                  </el-icon>
                  <span class="ml-2">{{ formatReadTime(article.read_time) }}</span>
                </span>
                <span class="flex items-center cursor-pointer" @click="handleLike">
                  <el-icon :class="isLiked ? 'liked-icon' : 'unliked-icon'" class="transition-colors">
                    <StarFilled v-if="isLiked" />
                    <Star v-else />
                  </el-icon>
                  <span class="ml-2">{{ likeCount }}</span>
                </span>
                <div class="flex gap-2">
                  <el-tag v-for="tag in article.tags" :key="tag" size="small" class="!rounded-button">
                    {{ tag }}
                  </el-tag>
                </div>
              </div>
              <div class="prose max-w-none">
                <div class="text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {{ article.content }}
                </div>
              </div>
            </article>
          </div>
          
          <!-- 评论区（编辑模式和查看模式都显示） -->
          <Comment :article-id="parseInt(route.params.id as string)" :is-editing="isEditing" />
        </div>

        <div v-else class="bg-white rounded-lg shadow-sm p-8 text-center">
          <el-icon class="text-4xl text-gray-400">
            <Warning />
          </el-icon>
          <h2 class="mt-4 text-xl font-bold text-gray-800">文章未找到</h2>
          <p class="mt-2 text-gray-600">抱歉，您要查看的文章不存在或已被删除。</p>
          <el-button @click="goBack" class="mt-4 !rounded-button">
            <el-icon class="mr-2">
              <ArrowLeft />
            </el-icon>
            返回首页
          </el-button>
        </div>
      </div>

      <!-- 数据加载中：显示空白 -->
      <div v-else>
        <!-- 数据加载完成前显示空白 -->
      </div>
    </main>
  </div>
</template>

<route>
{
  meta: {
    title: "文章详情 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, onMounted, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Calendar, Timer, ArrowLeft, Warning, Star, StarFilled, Folder, Edit, Delete, Check, Close } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { articleService, statisticService, programService } from '../../apis';
import EditArticle from '../../components/EditArticle.vue';

const route = useRoute();
const router = useRouter();

const article = ref(null);
const liking = ref(false);
const likeCount = ref(0);
const isLiked = ref(false); // 跟踪点赞状态
const dataLoaded = ref(false); // 标记数据是否已加载完成

// 编辑相关状态
const isEditing = ref(false);
const editLoading = ref(false);
const editArticleRef = ref();
const editForm = reactive({
  title: '',
  content: '',
  tags: [] as string[],
  readTime: 5,
  programId: null as number | null
});

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

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

// 加载文章详情和点赞数
const loadArticle = async () => {
  dataLoaded.value = false; // 重置数据加载状态
  try {
    const articleId = route.params.id;

    // 获取文章详情
    const articleResponse = await articleService.getArticle(articleId);
    article.value = articleResponse;

    // 获取文章列表数据来获取点赞数
    const articlesResponse = await articleService.getArticles();
    const currentArticle = articlesResponse.articles.find(a => a.id === parseInt(articleId));

    if (currentArticle) {
      likeCount.value = currentArticle.like_count;
      // 这里可以根据需要设置初始点赞状态
      // 在实际应用中，应该根据用户是否点赞过来设置 isLiked
    }

    // 标记数据加载完成
    dataLoaded.value = true;
  } catch (error) {
    article.value = null;
    // 即使出错也标记为已加载，以便显示错误状态
    dataLoaded.value = true;
  }
};

// 返回首页
const goBack = () => {
  router.push('/home');
};

// 增加浏览量
const incrementViewCount = async () => {
  try {
    const articleId = route.params.id;
    await statisticService.incrementViewCount(articleId);
  } catch (error) {
    console.error('增加浏览量失败:', error);
  }
};

// 处理点赞/取消点赞
const handleLike = async () => {
  if (liking.value) return;

  liking.value = true;
  try {
    const articleId = route.params.id;
    const action = isLiked.value ? 'unlike' : 'like';
    const response = await statisticService.toggleLikeCount(articleId, action);

    likeCount.value = response.like_count;
    isLiked.value = action === 'like';
  } catch (error) {
    console.error('点赞操作失败:', error);
  } finally {
    liking.value = false;
  }
};

// 跳转到项目页面
const goToProgram = async () => {
  if (!article.value?.program_name) return;

  try {
    // 获取所有项目
    const response = await programService.getAllProjects();
    const projects = response.projects || [];

    // 根据项目名称查找项目ID
    const project = projects.find(p => p.name === article.value.program_name);

    if (project) {
      // 跳转到项目详情页
      router.push(`/program/${project.id}`);
    } else {
      // 如果没有找到项目，跳转到项目列表页
      router.push('/program');
    }
  } catch (error) {
    console.error('获取项目列表失败:', error);
    // 出错时跳转到项目列表页
    router.push('/program');
  }
};

// 开始编辑
const startEdit = async () => {
  if (!article.value) return;
  
  // 获取项目ID（如果有）
  let programId = null;
  if (article.value.program_name) {
    try {
      const response = await programService.getAllProjects();
      const projects = response.projects || [];
      const project = projects.find(p => p.name === article.value.program_name);
      if (project) {
        programId = project.id;
      }
    } catch (error) {
      console.error('获取项目ID失败:', error);
    }
  }
  
  // 填充编辑表单
  editForm.title = article.value.title || '';
  editForm.content = article.value.content || '';
  editForm.tags = article.value.tags || [];
  editForm.readTime = article.value.read_time || 5;
  editForm.programId = programId;
  
  isEditing.value = true;
};

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false;
  editForm.title = '';
  editForm.content = '';
  editForm.tags = [];
  editForm.readTime = 5;
  editForm.programId = null;
};

// 保存编辑
const handleSaveEdit = async () => {
  if (editArticleRef.value) {
    // 调用EditArticle组件的提交方法
    const success = await editArticleRef.value.submitForm();
    if (success) {
      // 提交成功，handleUpdateArticle会被调用
      return;
    }
  }
};

// 处理文章更新
const handleUpdateArticle = async (articleData: any) => {
  try {
    const articleId = route.params.id;
    
    // 提取program_id（如果有）
    const programId = articleData.program_id;
    // 从articleData中移除program_id，因为更新接口不需要它
    const articleDataForUpdate = { ...articleData };
    delete articleDataForUpdate.program_id;
    
    // 调用API更新文章
    await articleService.updateArticle(articleId, articleDataForUpdate);
    
    // 处理项目关联逻辑
    try {
      // 获取当前文章的项目信息
      const currentProgramName = article.value?.program_name;
      
      // 如果选择了新项目
      if (programId) {
        // 获取项目信息
        const response = await programService.getAllProjects();
        const projects = response.projects || [];
        const project = projects.find(p => p.id === programId);
        
        if (project) {
          // 如果文章之前已经关联了其他项目，先移除
          if (currentProgramName && currentProgramName !== project.name) {
            const oldProject = projects.find(p => p.name === currentProgramName);
            if (oldProject) {
              await programService.removeArticleFromProject(oldProject.id, parseInt(articleId));
            }
          }
          
          // 只有当文章没有关联到当前项目时，才进行关联
          if (!currentProgramName || currentProgramName !== project.name) {
            await programService.addArticleToProject(programId, parseInt(articleId));
          }
        }
      } else if (currentProgramName) {
        // 如果取消了项目选择，但之前有关联项目，则移除关联
        const response = await programService.getAllProjects();
        const projects = response.projects || [];
        const project = projects.find(p => p.name === currentProgramName);
        if (project) {
          await programService.removeArticleFromProject(project.id, parseInt(articleId));
        }
      }
    } catch (projectError: any) {
      console.error('处理项目关联失败:', projectError);
      const errorMessage = projectError.response?.data?.error || '处理项目关联失败';
      ElMessage.warning(`文章更新成功，但${errorMessage}`);
    }

    ElMessage.success('文章更新成功！');
    
    // 重新加载文章数据
    await loadArticle();
    
    // 退出编辑模式
    isEditing.value = false;
    
  } catch (error: any) {
    console.error('更新文章失败:', error);
    console.error('错误详情:', error.response?.data);
    const errorMessage = error.response?.data?.error || '更新文章失败，请重试';
    ElMessage.error(errorMessage);
  } finally {
    editLoading.value = false;
  }
};

// 删除文章
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这篇文章吗？此操作不可撤销。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    const articleId = route.params.id;
    
    // 注意：这里需要先检查是否有删除文章的API，如果没有，可能需要先创建
    // 暂时假设有deleteArticle API
    await articleService.deleteArticle(articleId);

    ElMessage.success('文章删除成功！');

    // 跳转到首页
    router.push('/home');

  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除文章失败:', error);
      ElMessage.error(error.response?.data?.error || '删除文章失败，请重试');
    }
  }
};

onMounted(() => {
  loadArticle();
  incrementViewCount();
});
</script>

<style scoped>
.prose {
  max-width: none;
}

.prose img {
  margin: 0;
}

/* 点赞图标样式 - 使用高优先级选择器 */
.liked-icon {
  color: rgb(239 68 68) !important;
  /* text-red-500 */
}

.unliked-icon {
  color: rgb(107 114 128) !important;
  /* text-gray-500 */
}

.unliked-icon:hover {
  color: rgb(248 113 113) !important;
  /* text-red-400 */
}
</style>
