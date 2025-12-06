from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))  # 项目图片URL，格式：/static/uploads/projects/program{id}.{ext}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个项目可关联多个文章
    articles = db.relationship('Article', secondary='project_articles', back_populates='projects')


# 项目与文章的关联表（多对多关系）
class ProjectArticle(db.Model):
    __tablename__ = 'project_articles'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    read_time = db.Column(db.Integer, default=5)  # 单位：分钟
    view_count = db.Column(db.Integer, default=0)  # 浏览量
    like_count = db.Column(db.Integer, default=0)  # 点赞数
    comment_count = db.Column(db.Integer, default=0)  # 评论数
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    program_name = db.Column(db.String(200))  # 文章所属的项目名称

    # 标签关系
    tags = db.relationship('Tag', secondary='article_tags', back_populates='articles')

    # 项目关系（一个文章可以属于多个项目，也可以不属于任何项目）
    projects = db.relationship('Project', secondary='project_articles', back_populates='articles')


class ArticleTag(db.Model):
    __tablename__ = 'article_tags'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # 关系
    articles = db.relationship('Article', secondary='article_tags', back_populates='tags')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)

    # 关系
    article = db.relationship('Article', backref=db.backref('comments', lazy=True))
