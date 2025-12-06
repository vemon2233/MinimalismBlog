import api from './api.js'

// 项目相关API服务
export const programService = {
  // 获取所有项目（不分页）
  getAllProjects() {
    return api.get('/program/get-all')
  },
  
  // 获取单个项目详情
  getProject(id) {
    return api.get(`/program/single/${id}`)
  },
  
  // 创建项目
  createProject(data) {
    // 如果是FormData，不设置Content-Type，让浏览器自动设置
    const config = data instanceof FormData ? {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    } : {};
    return api.post('/program/create', data, config)
  },
  
  // 更新项目
  updateProject(id, data) {
    // 如果是FormData，不设置Content-Type，让浏览器自动设置
    const config = data instanceof FormData ? {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    } : {};
    return api.post(`/program/update/${id}`, data, config)
  },
  
  // 删除项目
  deleteProject(id) {
    return api.delete(`/program/delete/${id}`)
  },
  
  // 向项目添加文章
  addArticleToProject(projectId, articleId) {
    return api.post(`/program/${projectId}/add-article`, { article_id: articleId })
  },
  
  // 从项目中移除文章
  removeArticleFromProject(projectId, articleId) {
    return api.delete(`/program/${projectId}/remove-article/${articleId}`)
  }
}

export default programService
