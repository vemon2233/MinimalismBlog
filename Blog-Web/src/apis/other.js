import api from './api.js'

// 其他API服务
export const otherService = {
  // 获取所有标签
  getTags() {
    return api.get('/other/tag')
  }
}

export default otherService
