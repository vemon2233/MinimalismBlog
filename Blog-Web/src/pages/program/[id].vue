<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 pt-30 pb-12">
      <!-- 数据加载完成后的状态 -->
      <div v-if="dataLoaded">
        <!-- 错误状态 -->
        <ApiErrorState v-if="apiError" @retry="loadProjectData" />
        <div v-else>
          <!-- 项目介绍部分 -->
          <section class="max-w-7xl mx-4">
            <div class="bg-white rounded-xl shadow-md overflow-hidden">
              <div class="md:flex flex-wrap h-[280px]">
                <!-- 项目封面图片 -->
                <div class="md:flex-shrink-0 md:w-1/3 p-4">
                  <!-- 编辑模式：图片上传和预览 -->
                  <div v-if="isEditing" class="space-y-4 w-full h-full">
                    <!-- 上传图片 -->
                    <el-upload class="avatar-uploader w-full h-full" :action="uploadAction" :headers="uploadHeaders"
                      :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload"
                      accept=".png,.jpg,.jpeg,.gif,.webp">
                      <img v-if="editForm.imagePreview" :src="editForm.imagePreview"
                        class="w-full h-[248px] object-fill rounded-lg" />
                      <div v-else
                        class="w-full h-full flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors">
                        <div class="text-center">
                          <el-icon class="text-4xl text-gray-400 mb-2">
                            <Plus />
                          </el-icon>
                          <p class="text-sm text-gray-500">点击上传图片</p>
                          <p class="text-xs text-gray-400 mt-1">支持 PNG、JPG、JPEG、GIF、WEBP</p>
                          <p class="text-xs text-gray-400">大小不超过 5MB</p>
                        </div>
                      </div>
                    </el-upload>
                  </div>

                  <!-- 查看模式：显示图片 -->
                  <div v-else class="flex items-center justify-center h-full">
                    <img :src="project.image_url || 'http://localhost:5173/static/uploads/projects/not_found.png'"
                      class="w-full h-[248px] object-fill rounded-lg" :alt="project.name" />
                  </div>
                </div>
                <!-- 项目信息 -->
                <div class="p-8 md:w-2/3 md:flex-grow flex flex-col justify-between">
                  <div>
                    <div class="flex justify-between items-start">
                      <div>
                        <div class="uppercase tracking-wide text-sm text-indigo-500 font-semibold">项目</div>
                        <!-- 编辑模式：显示输入框 -->
                        <div v-if="isEditing" class="mt-1">
                          <el-input v-model="editForm.name" placeholder="项目名称" class="text-3xl font-bold" maxlength="20"
                            show-word-limit size="large" />
                        </div>
                        <!-- 查看模式：显示标题 -->
                        <h1 v-else class="mt-1 text-3xl font-bold text-gray-900">{{ project.name }}</h1>
                      </div>
                      <div class="flex gap-2">
                        <!-- 编辑模式：显示保存和取消按钮 -->
                        <div v-if="isEditing" class="flex gap-2">
                          <el-button type="success" plain :icon="Check" @click="handleSaveEdit" :loading="editLoading">
                            保存
                          </el-button>
                          <el-button :icon="Close" @click="cancelEdit">
                            取消
                          </el-button>
                        </div>
                        <!-- 查看模式：显示编辑和删除按钮 -->
                        <div v-else class="flex gap-2">
                          <el-button type="primary" plain :icon="Edit" @click="startEdit">
                            编辑
                          </el-button>
                          <el-button type="danger" plain :icon="Delete" @click="handleDelete">
                            删除
                          </el-button>
                        </div>
                      </div>
                    </div>

                    <!-- 编辑模式：显示描述输入框 -->
                    <div v-if="isEditing" class="mt-2">
                      <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="项目描述"
                        maxlength="200" show-word-limit />
                    </div>
                    <!-- 查看模式：显示描述 -->
                    <p v-else class="mt-2 text-gray-600">{{ project.description || '暂无项目描述' }}</p>
                  </div>

                  <div>
                    <div class="flex items-center">
                      <el-icon>
                        <Calendar />
                      </el-icon>
                      <span class="ml-2 text-gray-500">创建于 {{ formatDate(project.created_at) }}</span>
                    </div>
                    <div class="mt-2 flex items-center">
                      <el-icon>
                        <Document />
                      </el-icon>
                      <span class="ml-2 text-gray-500">包含 {{ project.article_count || 0 }} 篇文章</span>
                      <div class="ml-6 flex gap-2">
                        <el-button v-if="isEditing" type="success" link @click="navigateToAddArticle">
                          新增
                        </el-button>
                        <el-button v-if="isEditing" type="primary" link @click="handleAssociate">
                          关联
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 文章列表部分 -->
          <div class="max-w-7xl mx-auto px-4 pt-8 pb-12">
            <!-- 关联文章模式 -->
            <div v-if="isAssociating" class="space-y-6">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-gray-900">关联文章</h2>
                <el-button @click="cancelAssociate" plain>
                  <el-icon class="mr-2">
                    <ArrowLeft />
                  </el-icon>
                  返回
                </el-button>
              </div>

              <!-- 加载中 -->
              <div v-if="loadingAllArticles" class="bg-white rounded-lg shadow-sm p-8 text-center">
                <el-icon class="text-gray-400 text-4xl mb-4 animate-spin">
                  <Loading />
                </el-icon>
                <p class="text-gray-600">正在加载文章列表...</p>
              </div>

              <!-- 文章列表表格 -->
              <div v-else>
                <el-table :data="allArticles" class="w-full" stripe>
                  <el-table-column prop="title" label="文章标题" min-width="200">
                    <template #default="{ row }">
                      <div class="font-medium text-blue-600 hover:text-blue-800 cursor-pointer transition-colors"
                        @click="goToArticle(row.id)">
                        {{ row.title }}
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="created_at" label="创建时间" min-width="150">
                    <template #default="{ row }">
                      <div class="flex items-center text-gray-600">
                        <el-icon class="mr-1">
                          <Calendar />
                        </el-icon>
                        <span>{{ formatDate(row.created_at) }}</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="view_count" label="阅读量" width="120">
                    <template #default="{ row }">
                      <div class="flex items-center text-gray-600">
                        <el-icon class="mr-1">
                          <View />
                        </el-icon>
                        <span>{{ row.view_count || 0 }}</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="like_count" label="收藏量" width="120">
                    <template #default="{ row }">
                      <div class="flex items-center text-gray-600">
                        <el-icon class="mr-1">
                          <Star />
                        </el-icon>
                        <span>{{ row.like_count || 0 }}</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="comment_count" label="评论量" width="120">
                    <template #default="{ row }">
                      <div class="flex items-center text-gray-600">
                        <el-icon class="mr-1">
                          <ChatDotRound />
                        </el-icon>
                        <span>{{ row.comment_count || 0 }}</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="tags" label="标签" width="180">
                    <template #default="{ row }">
                      <div class="flex flex-wrap gap-1">
                        <el-tag v-for="tag in (row.tags || [])" :key="tag" size="small" class="mr-1 mb-1">
                          {{ tag }}
                        </el-tag>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="{ row }">
                      <div class="flex gap-2">
                        <el-button v-if="row.isAssociated" type="danger" plain size="small"
                          @click="unassociateArticle(row.id)" :icon="Close">
                          取消关联
                        </el-button>
                        <el-button v-else type="primary" plain size="small" @click="associateArticle(row.id)"
                          :icon="Link">
                          关联项目
                        </el-button>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>

                <!-- 分页组件 -->
                <div v-if="totalArticles > 0" class="flex justify-center mt-6">
                  <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="totalArticles"
                    layout="prev, pager, next" @current-change="handlePageChange" />
                </div>

                <!-- 无文章 -->
                <div v-if="allArticles.length === 0" class="bg-white rounded-lg shadow-sm p-8 text-center mt-4">
                  <el-icon class="text-gray-400 text-4xl mb-4">
                    <Document />
                  </el-icon>
                  <h3 class="text-xl font-bold text-gray-800 mb-2">暂无文章</h3>
                  <p class="text-gray-600">数据库中还没有文章</p>
                </div>
              </div>
            </div>

            <!-- 正常模式 -->
            <div v-else>
              <!-- 无文章状态 -->
              <div v-if="project.articles && project.articles.length === 0"
                class="bg-white rounded-lg shadow-sm p-8 text-center">
                <el-icon class="text-gray-400 text-4xl mb-4">
                  <Document />
                </el-icon>
                <h3 class="text-xl font-bold text-gray-800 mb-2">暂无文章</h3>
                <p class="text-gray-600">该项目目前还没有关联的文章</p>
              </div>

              <!-- 有文章状态 -->
              <div v-else class="space-y-6">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">项目文章</h2>
                <div v-for="article in project.articles" :key="article.id" class="relative">
                  <!-- 编辑模式下的删除按钮 -->
                  <div v-if="isEditing" class="absolute top-2 right-2 z-10">
                    <el-button type="danger" link @click.stop="removeArticleFromProject(article.id)">
                      移除
                    </el-button>
                  </div>
                  <SingleArticle :article="{
                    id: article.id,
                    title: article.title,
                    created_at: article.created_at,
                    read_time: article.read_time || 5,
                    view_count: article.view_count || 0,
                    like_count: article.like_count || 0,
                    comment_count: article.comment_count || 0,
                    excerpt: article.excerpt || '',
                    tags: article.tags || [],
                    program_name: article.program_name || ''
                  }" :show-program-name="false" @article-click="goToArticle" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据加载中 -->
      <div v-else>
        <!-- 数据加载完成前显示空白 -->
      </div>
    </div>
  </div>
</template>

<route>
{
  meta: {
    title: "项目详情 - 极简主义博客"
  }
}
</route>

<script lang="ts" setup>
import { ref, onMounted, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Calendar, Document, Edit, Delete, Star, Check, Close, ChatDotRound, Plus, Link, Loading, View, ArrowLeft } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import SingleArticle from '../../components/SingleArticle.vue';
import ApiErrorState from '../../components/ApiErrorState.vue';
import { programService } from '../../apis';
import { articleService } from '../../apis';

const route = useRoute();
const router = useRouter();

const project = ref({
  id: 0,
  name: '',
  description: '',
  image_url: '',
  created_at: '',
  updated_at: '',
  article_count: 0,
  articles: []
});
const dataLoaded = ref(false);
const apiError = ref(false);
const isEditing = ref(false);
const editLoading = ref(false);

// 关联文章相关状态
const isAssociating = ref(false);
const allArticles = ref<any[]>([]);
const loadingAllArticles = ref(false);

// 分页相关状态
const currentPage = ref(1);
const pageSize = ref(20);
const totalArticles = ref(0);
const allArticlesData = ref<any[]>([]);

// 编辑表单数据
const editForm = reactive({
  name: '',
  description: '',
  imageFile: null as File | null,
  imagePreview: '' as string,
  removeImage: false
});

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知日期';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 加载项目数据
const loadProjectData = async () => {
  dataLoaded.value = false;
  apiError.value = false;

  try {
    const projectId = route.params.id;

    // 调用后端的项目API
    const response = await programService.getProject(projectId);
    project.value = response;

  } catch (error) {
    console.error('加载项目数据失败:', error);
    apiError.value = true;
  } finally {
    dataLoaded.value = true;
  }
};

// 跳转到文章详情页
const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`);
};

// 监听路由变化
watch(
  () => route.params.id,
  () => {
    loadProjectData();
  }
);

// 开始编辑
const startEdit = () => {
  isEditing.value = true;
  editForm.name = project.value.name;
  editForm.description = project.value.description || '';
  editForm.imageFile = null;
  editForm.imagePreview = '';
  editForm.removeImage = false;
};

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false;
  isAssociating.value = false;
  editForm.name = '';
  editForm.description = '';
  editForm.imageFile = null;
  editForm.imagePreview = '';
  editForm.removeImage = false;
};

// 上传配置
const uploadAction = ref('/api/program/update/' + route.params.id);
const uploadHeaders = ref({
  'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
});

// 上传前验证
const beforeAvatarUpload = (file: File) => {
  const isImage = /\.(png|jpg|jpeg|gif|webp)$/i.test(file.name);
  const isLt5M = file.size / 1024 / 1024 < 5;

  if (!isImage) {
    ElMessage.error('只能上传图片文件！');
    return false;
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过5MB！');
    return false;
  }

  // 保存文件
  editForm.imageFile = file;

  // 创建预览
  const reader = new FileReader();
  reader.onload = (e) => {
    editForm.imagePreview = e.target?.result as string;
  };
  reader.readAsDataURL(file);

  return false; // 返回false，手动上传
};

// 处理上传成功
const handleAvatarSuccess = (response: any) => {
  // 这里不需要处理，因为我们手动上传
};

// 保存编辑
const handleSaveEdit = async () => {
  if (!editForm.name.trim()) {
    ElMessage.error('项目名称不能为空');
    return;
  }

  editLoading.value = true;

  try {
    // 创建FormData对象
    const formData = new FormData();
    formData.append('name', editForm.name.trim());
    formData.append('description', editForm.description.trim());

    // 处理图片删除
    if (editForm.removeImage) {
      formData.append('remove_image', 'true');
    }

    // 如果有新图片文件，添加到FormData
    if (editForm.imageFile) {
      formData.append('image', editForm.imageFile);
    }

    // 调用API更新项目
    const response = await programService.updateProject(project.value.id, formData);

    ElMessage.success('项目更新成功！');

    // 重新加载项目数据
    await loadProjectData();

    // 退出编辑模式
    isEditing.value = false;

  } catch (error: any) {
    console.error('更新项目失败:', error);
    ElMessage.error(error.response?.data?.error || '更新项目失败，请重试');
  } finally {
    editLoading.value = false;
  }
};

// 删除项目
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个项目吗？此操作不可撤销。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await programService.deleteProject(project.value.id);

    ElMessage.success('项目删除成功！');

    // 跳转到项目列表页面
    router.push('/program');

  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error);
      ElMessage.error(error.response?.data?.error || '删除项目失败，请重试');
    }
  }
};

// 从项目中移除文章
const removeArticleFromProject = async (articleId: number) => {
  try {
    await programService.removeArticleFromProject(project.value.id, articleId);

    ElMessage.success('文章已从项目中移除！');

    // 从本地数据中移除这篇文章
    project.value.articles = project.value.articles.filter(article => article.id !== articleId);

    // 更新文章数量
    project.value.article_count = project.value.articles.length;

  } catch (error: any) {
    console.error('移除文章失败:', error);
    ElMessage.error(error.response?.data?.error || '移除文章失败，请重试');
  }
};

// 跳转到新增文章页面
const navigateToAddArticle = () => {
  router.push({
    path: '/addarticle',
    query: { program_id: project.value.id }
  });
};

// 处理关联文章
const handleAssociate = async () => {
  isAssociating.value = true;
  loadingAllArticles.value = true;
  currentPage.value = 1;

  try {
    // 获取所有文章
    const response = await articleService.getAllArticles();
    const articlesData = response.articles || [];
    
    // 过滤掉已经关联了其他项目的文章（program_name不为空且不等于当前项目名称）
    const filteredArticles = articlesData.filter(article => {
      // 如果文章没有关联任何项目，可以显示
      if (!article.program_name) return true;
      // 如果文章已经关联到当前项目，可以显示
      if (article.program_name === project.value.name) return true;
      // 否则，文章关联了其他项目，不显示
      return false;
    });
    
    totalArticles.value = filteredArticles.length;

    // 标记哪些文章已经关联到当前项目
    const associatedArticleIds = new Set(project.value.articles.map(article => article.id));
    const markedArticles = filteredArticles.map(article => ({
      ...article,
      isAssociated: associatedArticleIds.has(article.id)
    }));

    // 保存完整文章数据用于分页
    allArticlesData.value = markedArticles;

    // 应用分页
    updatePagedArticles();

  } catch (error) {
    console.error('获取文章列表失败:', error);
    ElMessage.error('获取文章列表失败，请重试');
    isAssociating.value = false;
  } finally {
    loadingAllArticles.value = false;
  }
};

// 更新分页后的文章列表
const updatePagedArticles = () => {
  if (allArticlesData.value.length === 0) return;

  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  allArticles.value = allArticlesData.value.slice(startIndex, endIndex);
};

// 处理页码变化
const handlePageChange = (page: number) => {
  currentPage.value = page;
  updatePagedArticles();
};

// 取消关联模式
const cancelAssociate = () => {
  isAssociating.value = false;
  allArticles.value = [];
};

// 关联文章到项目
const associateArticle = async (articleId: number) => {
  try {
    await programService.addArticleToProject(project.value.id, articleId);

    // 更新本地状态
    const article = allArticles.value.find(a => a.id === articleId);
    if (article) {
      article.isAssociated = true;
    }

    // 更新项目文章列表
    if (article && !project.value.articles.some(a => a.id === articleId)) {
      project.value.articles.push(article);
      project.value.article_count = project.value.articles.length;
    }

    ElMessage.success('文章关联成功！');

  } catch (error: any) {
    console.error('关联文章失败:', error);
    ElMessage.error(error.response?.data?.error || '关联文章失败，请重试');
  }
};

// 取消文章关联
const unassociateArticle = async (articleId: number) => {
  try {
    await programService.removeArticleFromProject(project.value.id, articleId);

    // 更新本地状态
    const article = allArticles.value.find(a => a.id === articleId);
    if (article) {
      article.isAssociated = false;
    }

    // 更新项目文章列表
    project.value.articles = project.value.articles.filter(article => article.id !== articleId);
    project.value.article_count = project.value.articles.length;

    ElMessage.success('取消关联成功！');

  } catch (error: any) {
    console.error('取消关联失败:', error);
    ElMessage.error(error.response?.data?.error || '取消关联失败，请重试');
  }
};

// 页面加载时初始化
onMounted(() => {
  loadProjectData();
});
</script>

<style scoped>
/* 确保el-upload生成的div元素充满容器 */
:deep(.el-upload.el-upload--text) {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* 隐藏el-table的滚动条 */
:deep(.el-table__body-wrapper) {
  overflow-x: hidden !important;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar) {
  display: none !important;
}

:deep(.el-table__body-wrapper) {
  -ms-overflow-style: none !important;
  scrollbar-width: none !important;
}
</style>
