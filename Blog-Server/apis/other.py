from flask import Blueprint, jsonify
from models import Tag, ArticleTag
from sqlalchemy import func, desc

other_blueprint = Blueprint('other', __name__)


@other_blueprint.route('/tag', methods=['GET'])
def get_tags():
    """获取所有标签（按文章数量排序，返回前8个）"""
    try:
        # 查询标签及其关联的文章数量，按文章数量降序排序
        tags_with_count = Tag.query \
            .outerjoin(ArticleTag, Tag.id == ArticleTag.tag_id) \
            .group_by(Tag.id) \
            .order_by(desc(func.count(ArticleTag.id))) \
            .limit(8) \
            .all()

        # 构建返回数据，包含标签名称和文章数量
        tag_list = []
        for tag in tags_with_count:
            # 计算该标签的文章数量
            article_count = len(tag.articles)
            tag_list.append({
                'name': tag.name,
                'count': article_count
            })

        return jsonify({'tags': tag_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
