<template>
  <div class="edit-article-component">
    <div class="space-y-6">
      <!-- 标题 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">标题</label>
        <el-input
          v-model="articleForm.title"
          placeholder="请输入文章标题..."
          maxlength="20"
          show-word-limit
          class="text-xl font-bold"
          :class="{ 'border-red-300': errors.title }"
        />
        <div v-if="errors.title" class="text-red-500 text-sm mt-2">{{ errors.title }}</div>
      </div>

      <!-- 阅读时间 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">阅读时间（分钟）</label>
        <el-input
          v-model="articleForm.readTime"
          maxlength="2"
          oninput="value=value.replace(/[^0-9]/g,'')"
        />
      </div>

      <!-- 关联项目 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">关联项目</label>
        <el-select
          v-model="articleForm.programId"
          placeholder="选择关联的项目（可选）"
          class="w-full"
          clearable
          filterable
        >
          <el-option
            v-for="program in allPrograms"
            :key="program.id"
            :label="program.name"
            :value="program.id"
          />
        </el-select>
        <div class="text-xs text-gray-500 mt-1">
          选择文章所属的项目，如果不选择则表示文章不属于任何项目
        </div>
      </div>

      <!-- 标签 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
        <el-select
          v-model="articleForm.tags"
          multiple
          filterable
          allow-create
          default-first-option
          :reserve-keyword="false"
          placeholder="选择或输入文章标签"
          class="w-full"
        >
          <el-option
            v-for="tag in allTags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
      </div>

      <!-- 内容 -->
      <div>
        <div class="flex justify-between items-center mb-2">
          <label class="block text-sm font-medium text-gray-700">内容</label>
          <span class="text-xs text-gray-500">{{ articleForm.content.length }} 字符</span>
        </div>
        <el-input
          v-model="articleForm.content"
          type="textarea"
          :rows="20"
          placeholder="请输入文章内容..."
          maxlength="8000"
          show-word-limit
          :class="{ 'border-red-300': errors.content }"
        />
        <div v-if="errors.content" class="text-red-500 text-sm mt-2">{{ errors.content }}</div>
      </div>

      <!-- 错误提示 -->
      <div v-if="submitError" class="p-4 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100">
        {{ submitError }}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, defineProps, defineEmits, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { articleService, otherService, programService } from '../apis';

// 定义props
const props = defineProps({
  // 初始文章数据（用于编辑模式）
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      tags: [] as string[],
      readTime: 5,
      programId: null as number | null
    })
  },
  // 是否正在提交
  submitting: {
    type: Boolean,
    default: false
  }
});

// 定义emits
const emit = defineEmits<{
  'update:submitting': [value: boolean];
  'submit': [articleData: any];
}>();

// 表单数据
const articleForm = reactive({
  title: '',
  content: '',
  tags: [] as string[],
  readTime: 5,
  programId: null as number | null
});

// 错误信息
const errors = reactive({
  title: '',
  content: ''
});

// 提交错误
const submitError = ref('');

// 所有标签
const allTags = ref([]);

// 所有项目
const allPrograms = ref([]);

// 加载所有标签
const loadAllTags = async () => {
  try {
    const response = await otherService.getTags();
    // 从tags中提取标签名称（现在tags是对象数组，包含name和count）
    allTags.value = response.tags ? response.tags.map(tag => tag.name) : [];
  } catch (error) {
    console.error('加载标签失败:', error);
    allTags.value = [];
  }
};

// 加载所有项目
const loadAllPrograms = async () => {
  try {
    const response = await programService.getAllProjects();
    allPrograms.value = response.projects || [];
  } catch (error) {
    console.error('加载项目失败:', error);
    allPrograms.value = [];
  }
};

// 页面加载时获取数据
onMounted(() => {
  loadAllTags();
  loadAllPrograms();
  
  // 如果有初始数据，填充表单
  if (props.initialData) {
    articleForm.title = props.initialData.title || '';
    articleForm.content = props.initialData.content || '';
    articleForm.tags = props.initialData.tags || [];
    articleForm.readTime = props.initialData.readTime || 5;
    articleForm.programId = props.initialData.programId || null;
  }
});

// 监听初始数据变化
watch(() => props.initialData, (newData) => {
  if (newData) {
    articleForm.title = newData.title || '';
    articleForm.content = newData.content || '';
    articleForm.tags = newData.tags || [];
    articleForm.readTime = newData.readTime || 5;
    articleForm.programId = newData.programId || null;
  }
}, { deep: true });

// 验证表单
const validateForm = () => {
  let isValid = true;
  
  // 重置错误信息
  errors.title = '';
  errors.content = '';
  submitError.value = '';

  // 验证标题
  if (!articleForm.title.trim()) {
    errors.title = '标题不能为空';
    isValid = false;
  } else if (articleForm.title.trim().length < 3) {
    errors.title = '标题至少需要3个字符';
    isValid = false;
  }

  // 验证内容
  if (!articleForm.content.trim()) {
    errors.content = '内容不能为空';
    isValid = false;
  } else if (articleForm.content.trim().length < 10) {
    errors.content = '内容至少需要10个字符';
    isValid = false;
  }

  return isValid;
};

// 获取表单数据
const getFormData = () => {
  return {
    title: articleForm.title.trim(),
    excerpt: articleForm.content.slice(0, 150).replace(/[#*`]/g, '') + '...',
    content: articleForm.content.trim(),
    read_time: articleForm.readTime || 5,
    tags: articleForm.tags,
    program_id: articleForm.programId,
    is_published: true
  };
};

// 提交表单
const submitForm = async () => {
  if (!validateForm()) return false;

  emit('update:submitting', true);
  submitError.value = '';

  try {
    const formData = getFormData();
    emit('submit', formData);
    return true;
  } catch (error) {
    console.error('表单提交失败:', error);
    submitError.value = '提交失败，请重试';
    emit('update:submitting', false);
    return false;
  }
};

// 重置表单
const resetForm = () => {
  articleForm.title = '';
  articleForm.content = '';
  articleForm.tags = [];
  articleForm.readTime = 5;
  articleForm.programId = null;
  errors.title = '';
  errors.content = '';
  submitError.value = '';
};

// 暴露方法给父组件
defineExpose({
  submitForm,
  resetForm,
  getFormData,
  validateForm
});
</script>

<style scoped>
.edit-article-component {
  width: 100%;
}

:deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}

:deep(.el-textarea__inner) {
  border: 1px solid #e5e7eb !important;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05) !important;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
  line-height: 1.7 !important;
}

:deep(.el-textarea__inner:focus) {
  border-color: #57534e !important;
  box-shadow: 0 0 0 1px #57534e !important;
}
</style>
