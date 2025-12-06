from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
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
                'image_url': project.image_url,  # 添加图片URL字段
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
    """创建新项目（支持图片上传）"""
    try:
        # 获取表单数据
        name = request.form.get('name')
        description = request.form.get('description', '')
        article_ids_str = request.form.get('article_ids', '')
        
        # 验证必要字段
        if not name:
            return jsonify({'error': '项目名称不能为空'}), 400

        # 创建项目
        project = Project(
            name=name,
            description=description
        )

        db.session.add(project)
        db.session.flush()  # 获取project.id
        
        # 处理图片上传
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # 验证文件类型
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    # 获取文件扩展名
                    file_ext = file.filename.rsplit('.', 1)[1].lower()
                    
                    # 生成文件名：program{id}.{ext}
                    filename = f"program{project.id}.{file_ext}"
                    
                    # 创建上传目录
                    upload_dir = os.path.join('static', 'uploads', 'projects')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # 保存文件
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    
                    # 更新项目的image_url字段
                    project.image_url = f"/static/uploads/projects/{filename}"

        # 处理关联的文章（可选）
        if article_ids_str:
            try:
                article_ids = [int(id_str.strip()) for id_str in article_ids_str.split(',') if id_str.strip()]
                for article_id in article_ids:
                    # 验证文章是否存在
                    article = Article.query.get(article_id)
                    if article:
                        project_article = ProjectArticle(
                            project_id=project.id,
                            article_id=article_id
                        )
                        db.session.add(project_article)
            except ValueError:
                pass  # 忽略格式错误的article_ids

        db.session.commit()

        return jsonify({
            'message': '项目创建成功',
            'project_id': project.id,
            'image_url': project.image_url
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/single/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取单个项目详情"""
    try:
        project = Project.query.get_or_404(project_id)

        # 获取项目关联的文章（包含所有字段）
        articles = Article.query.join(ProjectArticle).filter(
            ProjectArticle.project_id == project_id
        ).order_by(Article.created_at.desc()).all()

        articles_list = []
        for article in articles:
            articles_list.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'excerpt': article.excerpt,
                'read_time': article.read_time,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'created_at': article.created_at.strftime('%Y-%m-%d'),
                'tags': [tag.name for tag in article.tags]
            })

        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'image_url': project.image_url,  # 添加图片URL字段
            'created_at': project.created_at.strftime('%Y-%m-%d'),
            'updated_at': project.updated_at.strftime('%Y-%m-%d') if project.updated_at else '',
            'articles': articles_list,
            'article_count': len(articles_list)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@program_blueprint.route('/update/<int:project_id>', methods=['POST'])
def update_project(project_id):
    """更新项目信息（支持图片上传）"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # 获取表单数据
        name = request.form.get('name')
        description = request.form.get('description')
        article_ids_str = request.form.get('article_ids', '')
        remove_image = request.form.get('remove_image', 'false').lower() == 'true'
        
        # 更新项目信息
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        
        # 处理图片删除
        if remove_image and project.image_url:
            # 删除物理文件
            file_path = os.path.join(project.image_url.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
            # 清空数据库字段
            project.image_url = None
        
        # 处理图片上传（新图片会覆盖旧图片）
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # 验证文件类型
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    # 获取文件扩展名
                    file_ext = file.filename.rsplit('.', 1)[1].lower()
                    
                    # 生成文件名：program{id}.{ext}
                    filename = f"program{project_id}.{file_ext}"
                    
                    # 创建上传目录
                    upload_dir = os.path.join('static', 'uploads', 'projects')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # 如果已有旧图片，先删除
                    if project.image_url:
                        old_file_path = os.path.join(project.image_url.lstrip('/'))
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    
                    # 保存新文件
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    
                    # 更新项目的image_url字段
                    project.image_url = f"/static/uploads/projects/{filename}"
        
        # 更新关联的文章（可选）
        # 只有当article_ids_str不为None且不为空字符串时才更新关联
        if article_ids_str is not None and article_ids_str != '':
            # 先删除现有的关联
            ProjectArticle.query.filter_by(project_id=project_id).delete()
            
            # 添加新的关联
            try:
                article_ids = [int(id_str.strip()) for id_str in article_ids_str.split(',') if id_str.strip()]
                for article_id in article_ids:
                    article = Article.query.get(article_id)
                    if article:
                        project_article = ProjectArticle(
                            project_id=project_id,
                            article_id=article_id
                        )
                        db.session.add(project_article)
            except ValueError:
                pass  # 忽略格式错误的article_ids

        db.session.commit()

        return jsonify({
            'message': '项目更新成功',
            'project_id': project.id,
            'image_url': project.image_url
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

        # 检查文章是否已经关联了其他项目（通过program_name字段）
        if article.program_name and article.program_name != project.name:
            return jsonify({'error': f'文章已关联到项目"{article.program_name}"，无法关联到新项目'}), 400

        # 检查是否已经关联（通过关联表）
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
        
        # 更新文章的program_name字段
        article.program_name = project.name
        
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

        # 获取文章并清除program_name字段
        article = Article.query.get(article_id)
        if article and article.program_name == project.name:
            article.program_name = None

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
