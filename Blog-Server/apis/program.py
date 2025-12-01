from flask import Blueprint, request, jsonify
from models import db, Project, Article, ProjectArticle

program_blueprint = Blueprint('program', __name__)


@program_blueprint.route('/get-all', methods=['GET'])
def get_all_projects():
    """获取所有项目（不分页）"""
    try:
        # 获取所有项目
        projects = Project.query.order_by(Project.created_at.desc()).all()

        # 批量获取每个项目关联的文章，避免N+1查询问题
        project_ids = [project.id for project in projects]
        project_articles = {}
        
        if project_ids:
            # 一次性获取所有项目关联的文章
            article_results = db.session.query(
                ProjectArticle.project_id,
                Article.id,
                Article.title,
                Article.created_at
            ).join(Article).filter(ProjectArticle.project_id.in_(project_ids)).all()

            for project_id, article_id, article_title, article_created_at in article_results:
                if project_id not in project_articles:
                    project_articles[project_id] = []
                project_articles[project_id].append({
                    'id': article_id,
                    'title': article_title,
                    'created_at': article_created_at.strftime('%Y-%m-%d') if article_created_at else ''
                })

        projects_list = []
        for project in projects:
            projects_list.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at.strftime('%Y-%m-%d'),
                'updated_at': project.updated_at.strftime('%Y-%m-%d') if project.updated_at else '',
                'article_count': len(project_articles.get(project.id, [])),
                'articles': project_articles.get(project.id, [])
            })

        return jsonify({
            'projects': projects_list,
            'total': len(projects_list)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/create', methods=['POST'])
def create_project():
    """创建新项目"""
    try:
        data = request.get_json()

        # 验证必要字段
        if not data.get('name'):
            return jsonify({'error': '项目名称不能为空'}), 400

        # 创建项目
        project = Project(
            name=data['name'],
            description=data.get('description', '')
        )

        db.session.add(project)
        db.session.flush()  # 获取project.id

        # 处理关联的文章（可选）
        if 'article_ids' in data and data['article_ids']:
            for article_id in data['article_ids']:
                # 验证文章是否存在
                article = Article.query.get(article_id)
                if article:
                    project_article = ProjectArticle(
                        project_id=project.id,
                        article_id=article_id
                    )
                    db.session.add(project_article)

        db.session.commit()

        return jsonify({
            'message': '项目创建成功',
            'project_id': project.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/single/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取单个项目详情"""
    try:
        project = Project.query.get_or_404(project_id)

        # 获取项目关联的文章
        articles = db.session.query(
            Article.id,
            Article.title,
            Article.excerpt,
            Article.created_at
        ).join(ProjectArticle).filter(
            ProjectArticle.project_id == project_id
        ).order_by(Article.created_at.desc()).all()

        articles_list = []
        for article in articles:
            articles_list.append({
                'id': article.id,
                'title': article.title,
                'excerpt': article.excerpt,
                'created_at': article.created_at.strftime('%Y-%m-%d') if article.created_at else ''
            })

        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.strftime('%Y-%m-%d'),
            'updated_at': project.updated_at.strftime('%Y-%m-%d') if project.updated_at else '',
            'articles': articles_list,
            'article_count': len(articles_list)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/update/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目信息"""
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()

        # 更新项目信息
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']

        # 更新关联的文章（可选）
        if 'article_ids' in data:
            # 先删除现有的关联
            ProjectArticle.query.filter_by(project_id=project_id).delete()
            
            # 添加新的关联
            if data['article_ids']:
                for article_id in data['article_ids']:
                    article = Article.query.get(article_id)
                    if article:
                        project_article = ProjectArticle(
                            project_id=project_id,
                            article_id=article_id
                        )
                        db.session.add(project_article)

        db.session.commit()

        return jsonify({
            'message': '项目更新成功',
            'project_id': project.id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/delete/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    try:
        project = Project.query.get_or_404(project_id)

        # 先删除关联关系
        ProjectArticle.query.filter_by(project_id=project_id).delete()
        
        # 删除项目
        db.session.delete(project)
        db.session.commit()

        return jsonify({
            'message': '项目删除成功'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/<int:project_id>/add-article', methods=['POST'])
def add_article_to_project(project_id):
    """向项目添加文章"""
    try:
        project = Project.query.get_or_404(project_id)
        data = request.get_json()

        if not data.get('article_id'):
            return jsonify({'error': '文章ID不能为空'}), 400

        article_id = data['article_id']
        
        # 验证文章是否存在
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404

        # 检查是否已经关联
        existing = ProjectArticle.query.filter_by(
            project_id=project_id,
            article_id=article_id
        ).first()
        
        if existing:
            return jsonify({'error': '文章已关联到该项目'}), 400

        # 创建关联
        project_article = ProjectArticle(
            project_id=project_id,
            article_id=article_id
        )
        
        db.session.add(project_article)
        db.session.commit()

        return jsonify({
            'message': '文章添加成功',
            'project_id': project_id,
            'article_id': article_id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/<int:project_id>/remove-article/<int:article_id>', methods=['DELETE'])
def remove_article_from_project(project_id, article_id):
    """从项目中移除文章"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # 检查关联是否存在
        project_article = ProjectArticle.query.filter_by(
            project_id=project_id,
            article_id=article_id
        ).first()
        
        if not project_article:
            return jsonify({'error': '文章未关联到该项目'}), 404

        # 删除关联
        db.session.delete(project_article)
        db.session.commit()

        return jsonify({
            'message': '文章移除成功',
            'project_id': project_id,
            'article_id': article_id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
