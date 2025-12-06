#!/usr/bin/env python3
"""
Program项目数据生成脚本
用于向数据库插入项目测试数据
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.insert(0, project_root)

from app import app, db
from models import Project, Article, ProjectArticle

# 项目数据
PROJECTS_DATA = [
    {
        "name": "探索未来科技趋势",
        "description": "本项目专注于分析最新的技术发展动态，涵盖人工智能、云计算和物联网等领域。通过深入研究和实践，探索技术如何改变我们的生活和工作方式。",
        "cover_image": "https://ai-public.mastergo.com/ai/img_res/fda1093c79b4c1dbcecb65102f40bbd2.jpg"
    },
    {
        "name": "Web全栈开发实战",
        "description": "从零开始构建完整的Web应用程序，涵盖前端Vue.js、后端Flask、数据库设计、部署运维等全流程。适合想要掌握全栈开发技能的开发者。",
        "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "数据科学与机器学习",
        "description": "学习数据科学的核心概念和机器学习算法，通过实际案例掌握数据清洗、特征工程、模型训练和评估的全过程。",
        "cover_image": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?ixlib=rb-4.0.3&auto=format&fit=crop&w-800&q=80"
    },
    {
        "name": "移动应用开发指南",
        "description": "涵盖iOS和Android平台的应用开发，学习React Native、Flutter等跨平台框架，以及原生开发的最佳实践。",
        "cover_image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "DevOps与云原生",
        "description": "学习现代软件开发和运维的最佳实践，包括Docker容器化、Kubernetes编排、CI/CD流水线和云服务的使用。",
        "cover_image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    }
]

def generate_projects():
    """生成项目数据"""
    print("生成项目数据...")
    projects = []
    
    for i, project_data in enumerate(PROJECTS_DATA):
        # 随机生成创建时间（最近90天内）
        days_ago = random.randint(0, 90)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        project = Project(
            name=project_data["name"],
            description=project_data["description"],
            created_at=created_at
        )
        
        projects.append(project)
        print(f"  创建项目: {project_data['name']}")
    
    return projects

def assign_articles_to_projects(projects, articles):
    """为项目分配文章"""
    print("为项目分配文章...")
    project_articles = []
    
    # 确保有足够的文章
    if len(articles) < 3:
        print("  错误：文章数量不足，无法分配")
        return project_articles
    
    for project in projects:
        # 每个项目分配3-6篇文章
        num_articles = random.randint(3, 6)
        
        # 随机选择文章（确保不重复选择同一篇文章给同一项目）
        available_articles = articles.copy()
        selected_articles = []
        
        for _ in range(min(num_articles, len(available_articles))):
            if not available_articles:
                break
            article = random.choice(available_articles)
            selected_articles.append(article)
            available_articles.remove(article)
        
        for article in selected_articles:
            project_article = ProjectArticle(
                project_id=project.id,
                article_id=article.id
            )
            project_articles.append(project_article)
        
        article_titles = [article.title for article in selected_articles]
        print(f"  项目 '{project.name}' 分配文章: {len(selected_articles)}篇")
        for title in article_titles[:3]:  # 只显示前3篇文章标题
            print(f"    - {title}")
        if len(article_titles) > 3:
            print(f"    ... 还有 {len(article_titles) - 3} 篇")
    
    return project_articles

def main():
    """主函数"""
    print("开始生成Program项目数据...")
    print("=" * 50)
    
    with app.app_context():
        # 获取现有的文章
        articles = Article.query.all()
        if not articles:
            print("错误：数据库中没有文章数据，请先运行seed_data.py生成文章数据")
            return
        
        print(f"找到 {len(articles)} 篇文章")
        
        # 生成项目
        projects = generate_projects()
        
        # 添加到数据库
        print("\n将项目数据添加到数据库...")
        db.session.add_all(projects)
        db.session.commit()
        print("  项目已保存")
        
        # 为项目分配文章
        project_articles = assign_articles_to_projects(projects, articles)
        if project_articles:
            db.session.add_all(project_articles)
            db.session.commit()
            print("  项目-文章关系已保存")
        
        # 统计信息
        print("\n" + "=" * 50)
        print("Program项目数据生成完成！")
        print(f"  生成项目数: {len(projects)}")
        print(f"  项目-文章关系数: {len(project_articles)}")
        
        # 显示项目详情
        print("\n生成的项目详情:")
        for project in projects:
            article_count = len([pa for pa in project_articles if pa.project_id == project.id])
            print(f"\n项目: {project.name}")
            print(f"  描述: {project.description[:50]}...")
            print(f"  创建时间: {project.created_at.strftime('%Y-%m-%d')}")
            print(f"  关联文章数: {article_count}")
            print(f"  访问URL: /program/{project.id}")

if __name__ == "__main__":
    # 检查是否在正确的目录中运行
    app_path = os.path.join(project_root, "app.py")
    if not os.path.exists(app_path):
        print("错误：找不到app.py文件")
        print("项目根目录:", project_root)
        print("当前目录:", os.getcwd())
        sys.exit(1)
    
    # 确认操作
    print("警告：此脚本将向数据库插入Program项目数据。")
    print("请确保数据库已有文章数据（可先运行seed_data.py）。")
    
    # 自动确认（用于非交互式运行）
    import getpass
    if getpass.getuser() != "":  # 非交互式环境
        response = 'y'
    else:
        response = input("是否继续？(y/N): ").strip().lower()
    
    if response != 'y':
        print("操作已取消")
        sys.exit(0)
    
    try:
        main()
    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
