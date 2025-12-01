import api from './api.js'

// 评论相关API服务
export const commentService = {
  // 获取文章评论
  getComments(articleId) {
    return api.get(`/comment/get-all/${articleId}`)
  },

  // 创建评论
  createComment(articleId, data) {
    return api.post(`/comment/create/${articleId}`, data)
  },

  // 删除评论
  deleteComment(commentId) {
    return api.delete(`/comment/delete/${commentId}`)
  }
}

export default commentService
