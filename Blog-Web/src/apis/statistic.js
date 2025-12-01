import api from './api.js'

// 统计相关API服务
export const statisticService = {
  // 增加文章浏览量
  incrementViewCount(articleId) {
    return api.post(`/statistic/${articleId}/view`)
  },

  // 切换文章点赞状态
  toggleLikeCount(articleId, action = 'like') {
    return api.post(`/statistic/${articleId}/like`, { action })
  }
}

export default statisticService
