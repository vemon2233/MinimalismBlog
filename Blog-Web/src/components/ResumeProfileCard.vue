<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <div class="flex flex-col items-center">
      <div class="w-48 h-48 rounded-full overflow-hidden mb-4">
        <img :src="avatarUrl" alt="个人照片" class="w-full h-full object-cover" />
      </div>
      <h1 class="text-2xl font-bold mb-2">陈思远</h1>
      <p class="text-gray-600 text-center mb-6">
        资深前端工程师，5年+工作经验，
        专注于构建高性能的Web应用
      </p>
    </div>

    <!-- 联系方式 -->
    <div class="flex justify-center gap-4 mt-8">
      <el-tooltip content="微信" placement="top">
        <el-button class="!rounded-button contact-btn" @click="showQRCode('wechat')">
          <el-icon>
            <ChatRound />
          </el-icon>
        </el-button>
      </el-tooltip>
      <el-tooltip content="QQ" placement="top">
        <el-button class="!rounded-button contact-btn" @click="showQRCode('qq')">
          <el-icon>
            <Monitor />
          </el-icon>
        </el-button>
      </el-tooltip>
      <el-tooltip content="电话" placement="top">
        <el-button class="!rounded-button contact-btn" @click="showContact('phone')">
          <el-icon>
            <Phone />
          </el-icon>
        </el-button>
      </el-tooltip>
      <el-tooltip content="邮箱" placement="top">
        <el-button class="!rounded-button contact-btn" @click="showContact('email')">
          <el-icon>
            <Message />
          </el-icon>
        </el-button>
      </el-tooltip>
    </div>

    <!-- 二维码弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="360px" align-center>
      <div class="text-center">
        <template v-if="dialogType === 'wechat' || dialogType === 'qq'">
          <img :src="qrCodeUrl" :alt="dialogTitle" class="w-64 h-64 mx-auto" />
        </template>
        <template v-else>
          <p class="text-xl">{{ contactInfo }}</p>
        </template>
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { ChatRound, Monitor, Phone, Message } from '@element-plus/icons-vue';
const dialogVisible = ref(false);
const dialogTitle = ref('');
const dialogType = ref('');
const qrCodeUrl = ref('');
const contactInfo = ref('');

const avatarUrl = 'https://ai-public.mastergo.com/ai/img_res/63339e8190ac10c16c54bb69bae206e1.jpg';
const showQRCode = (type: string) => {
  dialogType.value = type;
  dialogTitle.value = type === 'wechat' ? '微信二维码' : 'QQ二维码';
  qrCodeUrl.value = `https://mastergo.com/ai/api/search-image?query=clean and simple QR code design on white background&width=400&height=400&orientation=squarish&flag=e856ce31d7583f01614d95b6c113c978`;
  dialogVisible.value = true;
};

const showContact = (type: string) => {
  dialogType.value = type;
  if (type === 'phone') {
    dialogTitle.value = '联系电话';
    contactInfo.value = '138 8888 8888';
  } else {
    dialogTitle.value = '电子邮箱';
    contactInfo.value = 'contact@example.com';
  }
  dialogVisible.value = true;
};
</script>

<style scoped>
.el-dialog {
  border-radius: 16px;
}
</style>