import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import pinia from './modules/pinia'
import router from './modules/router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
// 全局状态管理
app.use(pinia)
// 路由管理
app.use(router)
// Element Plus
app.use(ElementPlus)
app.mount('#app')
