#!/usr/bin/env python3
"""
检查数据库中的数据
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Article, Tag, Comment, ArticleTag

def check_data():
    """检查数据库中的数据"""
    print("检查数据库中的数据...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 统计各表数据量
            article_count = Article.query.count()
            tag_count = Tag.query.count()
            comment_count = Comment.query.count()
            article_tag_count = ArticleTag.query.count()
            
            print(f"文章数量: {article_count}")
            print(f"标签数量: {tag_count}")
            print(f"评论数量: {comment_count}")
            print(f"文章-标签关系数量: {article_tag_count}")
            
            print("\n" + "=" * 50)
            print("文章列表:")
            print("-" * 50)
            
            # 显示前5篇文章
            articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
            for article in articles:
                tags = [tag.name for tag in article.tags]
                print(f"ID: {article.id}")
                print(f"标题: {article.title}")
                print(f"浏览量: {article.view_count}, 点赞: {article.like_count}, 评论: {article.comment_count}")
                print(f"标签: {', '.join(tags)}")
                print(f"创建时间: {article.created_at}")
                print("-" * 30)
            
            print("\n" + "=" * 50)
            print("标签列表:")
            print("-" * 50)
            
            # 显示所有标签及其文章数量
            tags = Tag.query.all()
            for tag in tags:
                article_count = len(tag.articles)
                print(f"{tag.name}: {article_count} 篇文章")
            
            print("\n" + "=" * 50)
            print("数据检查完成！")
            
        except Exception as e:
            print(f"检查数据时出错: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    check_data()
