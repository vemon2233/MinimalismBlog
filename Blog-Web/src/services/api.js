import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Flask后端地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// API服务
export const articleService = {
  // 获取文章列表
  getArticles(params = {}) {
    return api.get('/articles', { params })
  },
  
  // 获取单篇文章
  getArticle(id) {
    return api.get(`/articles/${id}`)
  },
  
  // 创建文章
  createArticle(data) {
    return api.post('/articles', data)
  },
  
  // 获取所有标签
  getTags() {
    return api.get('/tags')
  },
  
  // 获取热门文章
  getHotArticles() {
    return api.get('/hot-articles')
  },

  // 获取文章归档
  getArchives() {
    return api.get('/archives')
  },

  // 评论相关API
  // 获取文章评论
  getComments(articleId) {
    return api.get(`/articles/${articleId}/comments`)
  },

  // 创建评论
  createComment(articleId, data) {
    return api.post(`/articles/${articleId}/comments`, data)
  },

  // 删除评论
  deleteComment(commentId) {
    return api.delete(`/comments/${commentId}`)
  },

  // 增加文章浏览量
  incrementViewCount(articleId) {
    return api.post(`/articles/${articleId}/view`)
  },

  // 切换文章点赞状态
  toggleLikeCount(articleId, action = 'like') {
    return api.post(`/articles/${articleId}/like`, { action })
  },

  // 搜索文章
  searchArticles(params = {}) {
    return api.get('/search', { params })
  }
}

export default api
