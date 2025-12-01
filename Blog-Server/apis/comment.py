from flask import Blueprint, request, jsonify
from models import db, Article, Comment

comment_blueprint = Blueprint('comment', __name__)


# 评论相关API
@comment_blueprint.route('/get-all/<int:article_id>', methods=['GET'])
def get_comments(article_id):
    """获取文章的所有评论"""
    try:
        comments = Comment.query.filter_by(
            article_id=article_id,
            is_approved=True
        ).order_by(Comment.created_at.desc()).all()

        comment_list = []
        for comment in comments:
            comment_list.append({
                'id': comment.id,
                'author_name': comment.author_name,
                'author_email': comment.author_email,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify({'comments': comment_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@comment_blueprint.route('/create/<int:article_id>', methods=['POST'])
def create_comment(article_id):
    """创建新评论"""
    try:
        data = request.get_json()

        # 验证文章是否存在
        article = Article.query.get_or_404(article_id)

        # 创建评论
        comment = Comment(
            article_id=article_id,
            author_name=data['author_name'],
            author_email=data.get('author_email', ''),
            content=data['content']
        )

        db.session.add(comment)

        # 更新文章的评论计数
        article.comment_count += 1
        db.session.commit()

        return jsonify({
            'message': '评论提交成功',
            'comment_id': comment.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@comment_blueprint.route('/delete/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """删除评论（管理员功能）"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': '评论删除成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
