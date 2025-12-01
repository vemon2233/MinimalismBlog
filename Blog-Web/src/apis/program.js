import api from './api.js'

// 项目相关API服务
export const programService = {
  // 获取所有项目（不分页）
  getAllProjects() {
    return api.get('/program/get-all')
  },
  
  // 获取单个项目详情
  getProject(id) {
    return api.get(`/program/${id}`)
  },
  
  // 创建项目
  createProject(data) {
    return api.post('/program/create', data)
  },
  
  // 更新项目
  updateProject(id, data) {
    return api.put(`/program/${id}/update`, data)
  },
  
  // 删除项目
  deleteProject(id) {
    return api.delete(`/program/${id}/delete`)
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
