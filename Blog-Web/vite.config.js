import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// pages引入页面路由管理
import Pages from 'vite-plugin-pages'
// components引入管理，后续无需手动引入component
import Components from 'unplugin-vue-components/vite'
// autoimport引入vue等内容，后续无需再手动写
import AutoImport from 'unplugin-auto-import/vite'
import { AntDesignVueResolver, ElementPlusResolver, VantResolver, NaiveUiResolver } from 'unplugin-vue-components/resolvers'
// 导入tailwindcss
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Pages(),
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia']
    }),
    Components({
      resolvers: [AntDesignVueResolver(), ElementPlusResolver(), VantResolver(), NaiveUiResolver()],
    }),
    tailwindcss(),
  ],
  server: {
    proxy: {
      // 代理静态文件请求到Flask后端
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
