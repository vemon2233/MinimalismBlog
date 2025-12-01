from flask import Blueprint, request, jsonify
from models import db, Article, Tag, ArticleTag

article_blueprint = Blueprint('article', __name__)


@article_blueprint.route('/get-page', methods=['GET'])
def get_articles():
    """获取文章列表（分页）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        tag = request.args.get('tag', '')
        archive = request.args.get('archive', '')

        # 构建查询
        query = Article.query.filter_by(is_published=True)

        # 按标签筛选
        if tag:
            query = query.join(ArticleTag).join(Tag).filter(Tag.name == tag)

        # 按归档月份筛选
        if archive:
            # 将"2025年11月"转换为"2025-11"格式进行查询
            year_month = archive.replace('年', '-').replace('月', '')
            query = query.filter(
                db.func.DATE_FORMAT(Article.created_at, '%Y-%m') == year_month
            )

        # 分页查询
        pagination = query.order_by(Article.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        # 批量获取标签，避免N+1查询问题
        article_ids = [article.id for article in pagination.items]
        article_tags = {}
        if article_ids:
            # 一次性获取所有文章的标签
            tag_results = db.session.query(
                ArticleTag.article_id,
                Tag.name
            ).join(Tag).filter(ArticleTag.article_id.in_(article_ids)).all()

            for article_id, tag_name in tag_results:
                if article_id not in article_tags:
                    article_tags[article_id] = []
                article_tags[article_id].append(tag_name)

        articles = []
        for article in pagination.items:
            articles.append({
                'id': article.id,
                'title': article.title,
                'excerpt': article.excerpt,
                'read_time': article.read_time,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'created_at': article.created_at.strftime('%Y-%m-%d'),
                'tags': article_tags.get(article.id, [])
            })

        return jsonify({
            'articles': articles,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/all-articles', methods=['GET'])
def get_all_articles():
    """获取所有文章（不分页，用于归档页面）"""
    try:
        # 获取所有已发布文章
        articles = Article.query.filter_by(is_published=True) \
            .order_by(Article.created_at.desc()) \
            .all()

        # 批量获取标签，避免N+1查询问题
        article_ids = [article.id for article in articles]
        article_tags = {}
        if article_ids:
            # 一次性获取所有文章的标签
            tag_results = db.session.query(
                ArticleTag.article_id,
                Tag.name
            ).join(Tag).filter(ArticleTag.article_id.in_(article_ids)).all()

            for article_id, tag_name in tag_results:
                if article_id not in article_tags:
                    article_tags[article_id] = []
                article_tags[article_id].append(tag_name)

        articles_list = []
        for article in articles:
            articles_list.append({
                'id': article.id,
                'title': article.title,
                'excerpt': article.excerpt,
                'read_time': article.read_time,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'created_at': article.created_at.strftime('%Y-%m-%d'),
                'tags': article_tags.get(article.id, [])
            })

        return jsonify({
            'articles': articles_list,
            'total': len(articles_list)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/single/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """获取单篇文章详情"""
    try:
        article = Article.query.get_or_404(article_id)

        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'excerpt': article.excerpt,
            'read_time': article.read_time,
            'created_at': article.created_at.strftime('%Y-%m-%d'),
            'tags': [tag.name for tag in article.tags]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/create', methods=['POST'])
def create_article():
    """创建新文章"""
    try:
        data = request.get_json()

        # 创建文章
        article = Article(
            title=data['title'],
            content=data['content'],
            excerpt=data.get('excerpt', ''),
            read_time=data.get('read_time', 5),  # 默认5分钟
            is_published=data.get('is_published', True)
        )

        db.session.add(article)
        db.session.flush()  # 获取article.id

        # 处理标签
        if 'tags' in data:
            for tag_name in data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()

                article_tag = ArticleTag(article_id=article.id, tag_id=tag.id)
                db.session.add(article_tag)

        db.session.commit()

        return jsonify({
            'message': '文章创建成功',
            'article_id': article.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/hot-articles', methods=['GET'])
def get_hot_articles():
    """获取热门文章（按浏览量排序的前4篇文章）"""
    try:
        articles = Article.query.filter_by(is_published=True) \
            .order_by(Article.view_count.desc()) \
            .limit(4) \
            .all()

        hot_articles = []
        for article in articles:
            hot_articles.append({
                'id': article.id,
                'title': article.title,
                'view_count': article.view_count
            })

        return jsonify({'hot_articles': hot_articles})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/archives', methods=['GET'])
def get_archives():
    """获取文章归档数据（按月分组）"""
    try:
        # 获取所有已发布文章
        articles = Article.query.filter_by(is_published=True).all()

        # 手动按月份分组统计
        archive_dict = {}
        for article in articles:
            # 格式化月份：YYYY年MM月
            month = article.created_at.strftime('%Y年%m月')
            if month in archive_dict:
                archive_dict[month] += 1
            else:
                archive_dict[month] = 1

        # 转换为列表并按月份排序（降序）
        archive_list = []
        for month, count in archive_dict.items():
            archive_list.append({
                'date': month,
                'count': count
            })

        # 按日期降序排序
        archive_list.sort(key=lambda x: x['date'], reverse=True)

        return jsonify({'archives': archive_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@article_blueprint.route('/search', methods=['GET'])
def search_articles():
    """搜索文章（按标题或标签）"""
    try:
        query = request.args.get('query', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if not query:
            return jsonify({
                'articles': [],
                'total': 0,
                'pages': 0,
                'current_page': page
            })

        # 构建搜索查询
        search_query = Article.query.filter_by(is_published=True)

        # 按标题搜索（模糊匹配）
        title_query = Article.title.ilike(f'%{query}%')

        # 按标签搜索
        tag_query = Article.query.join(ArticleTag).join(Tag).filter(Tag.name.ilike(f'%{query}%'))

        # 合并两个查询结果（去重）
        articles_from_title = search_query.filter(title_query).all()
        articles_from_tags = tag_query.all()

        # 合并结果并去重
        all_articles = list(set(articles_from_title + articles_from_tags))

        # 手动分页
        total = len(all_articles)
        pages = (total + per_page - 1) // per_page  # 向上取整
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_articles = all_articles[start_index:end_index]

        # 批量获取标签，避免N+1查询问题
        article_ids = [article.id for article in paginated_articles]
        article_tags = {}
        if article_ids:
            # 一次性获取所有文章的标签
            tag_results = db.session.query(
                ArticleTag.article_id,
                Tag.name
            ).join(Tag).filter(ArticleTag.article_id.in_(article_ids)).all()

            for article_id, tag_name in tag_results:
                if article_id not in article_tags:
                    article_tags[article_id] = []
                article_tags[article_id].append(tag_name)

        articles = []
        for article in paginated_articles:
            articles.append({
                'id': article.id,
                'title': article.title,
                'excerpt': article.excerpt,
                'read_time': article.read_time,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'created_at': article.created_at.strftime('%Y-%m-%d'),
                'tags': article_tags.get(article.id, [])
            })

        return jsonify({
            'articles': articles,
            'total': total,
            'pages': pages,
            'current_page': page
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
