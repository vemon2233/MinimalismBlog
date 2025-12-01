from flask import Blueprint, request, jsonify
from models import db, Article

statistic_blueprint = Blueprint('statistic', __name__)


@statistic_blueprint.route('/<int:article_id>/view', methods=['POST'])
def increment_view_count(article_id):
    """增加文章浏览量"""
    try:
        article = Article.query.get_or_404(article_id)
        article.view_count += 1
        db.session.commit()

        return jsonify({
            'message': '浏览量增加成功',
            'view_count': article.view_count
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@statistic_blueprint.route('/<int:article_id>/like', methods=['POST'])
def toggle_like_count(article_id):
    """切换文章点赞状态"""
    try:
        article = Article.query.get_or_404(article_id)

        # 获取请求数据，判断是点赞还是取消点赞
        data = request.get_json() or {}
        action = data.get('action', 'like')  # like 或 unlike

        if action == 'like':
            article.like_count += 1
            message = '点赞成功'
        else:
            article.like_count = max(0, article.like_count - 1)  # 确保不会变成负数
            message = '取消点赞成功'

        db.session.commit()

        return jsonify({
            'message': message,
            'like_count': article.like_count,
            'action': action
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500