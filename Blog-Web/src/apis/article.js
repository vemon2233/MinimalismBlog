import api from './api.js'

// 文章相关API服务
export const articleService = {
  // 获取文章列表（分页）
  getArticles(params = {}) {
    return api.get('/article/get-page', { params })
  },
  
  // 获取所有文章（不分页，用于归档页面）
  getAllArticles() {
    return api.get('/article/all-articles')
  },
  
  // 获取单篇文章
  getArticle(id) {
    return api.get(`/article/single/${id}`)
  },
  
  // 创建文章
  createArticle(data) {
    return api.post('/article/create', data)
  },
  
  // 获取热门文章
  getHotArticles() {
    return api.get('/article/hot-articles')
  },

  // 获取文章归档
  getArchives() {
    return api.get('/article/archives')
  },

  // 搜索文章
  searchArticles(params = {}) {
    return api.get('/article/search', { params })
  },

  // 更新文章
  updateArticle(id, data) {
    return api.put(`/article/update/${id}`, data)
  },

  // 删除文章
  deleteArticle(id) {
    return api.delete(`/article/delete/${id}`)
  }
}

export default articleService
