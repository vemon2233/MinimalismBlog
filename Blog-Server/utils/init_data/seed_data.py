#!/usr/bin/env python3
"""
数据库模拟数据生成脚本
用于向数据库插入测试数据
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Article, Tag, ArticleTag, Comment

# 模拟数据配置
NUM_ARTICLES = 20
NUM_TAGS = 10
COMMENTS_PER_ARTICLE = 3

# 文章标题模板
ARTICLE_TITLES = [
    "Python编程入门指南",
    "Vue.js前端开发实战",
    "Flask后端API设计",
    "数据库优化技巧",
    "Web安全最佳实践",
    "机器学习基础教程",
    "Docker容器化部署",
    "RESTful API设计原则",
    "前端性能优化策略",
    "微服务架构设计",
    "React Hooks使用指南",
    "TypeScript类型系统详解",
    "Git工作流最佳实践",
    "CI/CD流水线搭建",
    "云计算基础概念",
    "数据结构与算法",
    "Linux系统管理",
    "网络安全防护",
    "移动应用开发",
    "人工智能应用场景"
]

# 文章内容模板
ARTICLE_CONTENT = """
## {title}

这是一篇关于{title}的示例文章内容。

### 章节一：概述
{title}是现代软件开发中的重要组成部分。本文将详细介绍相关概念和实践。

### 章节二：核心概念
1. **基础概念**：理解{title}的基本原理
2. **实践应用**：在实际项目中的应用场景
3. **最佳实践**：行业内的最佳实践方法

### 章节三：代码示例
```python
def example_function():
    \"\"\"示例函数\"\"\"
    print("Hello, {title}!")
    return True
```

### 章节四：总结
通过本文的学习，您应该对{title}有了更深入的理解。建议结合实际项目进行练习。

---

*本文为模拟数据，仅用于测试目的。*
"""

# 标签列表
TAG_NAMES = [
    "Python", "Vue", "Flask", "数据库", "前端",
    "后端", "DevOps", "机器学习", "安全", "工具"
]

# 评论作者
AUTHOR_NAMES = [
    "张三", "李四", "王五", "赵六", "钱七",
    "孙八", "周九", "吴十", "郑十一", "王十二"
]

# 评论内容模板
COMMENT_TEMPLATES = [
    "很好的文章，学到了很多！",
    "感谢分享，对我帮助很大。",
    "内容很详细，期待更多相关文章。",
    "有几个地方不太明白，能详细解释一下吗？",
    "实践了一下，效果不错！",
    "文章结构清晰，易于理解。",
    "希望能有更多实战案例。",
    "这个技术点讲得很透彻。",
    "对我当前的项目很有帮助。",
    "期待作者的下一篇文章。"
]

def generate_articles():
    """生成文章数据"""
    print("生成文章数据...")
    articles = []
    
    for i in range(NUM_ARTICLES):
        # 随机选择标题
        title = ARTICLE_TITLES[i % len(ARTICLE_TITLES)]
        if i >= len(ARTICLE_TITLES):
            title = f"{title}（第{i//len(ARTICLE_TITLES)+1}部分）"
        
        # 生成文章内容
        content = ARTICLE_CONTENT.format(title=title)
        excerpt = f"{title}的简要介绍。本文将深入探讨相关技术和实践应用。"
        
        # 随机生成阅读时间（3-15分钟）
        read_time = random.randint(3, 15)
        
        # 随机生成浏览量、点赞数、评论数
        view_count = random.randint(50, 1000)
        like_count = random.randint(10, 200)
        comment_count = random.randint(0, 50)
        
        # 随机生成创建时间（最近180天内）
        days_ago = random.randint(0, 180)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        article = Article(
            title=title,
            content=content,
            excerpt=excerpt,
            read_time=read_time,
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count,
            created_at=created_at,
            is_published=True
        )
        
        articles.append(article)
        print(f"  创建文章: {title}")
    
    return articles

def generate_tags():
    """生成标签数据"""
    print("生成标签数据...")
    tags = []
    
    for tag_name in TAG_NAMES:
        tag = Tag(name=tag_name)
        tags.append(tag)
        print(f"  创建标签: {tag_name}")
    
    return tags

def assign_tags_to_articles(articles, tags):
    """为文章分配标签"""
    print("为文章分配标签...")
    article_tags = []
    
    for article in articles:
        # 每篇文章分配2-4个随机标签
        num_tags = random.randint(2, 4)
        selected_tags = random.sample(tags, min(num_tags, len(tags)))
        
        for tag in selected_tags:
            article_tag = ArticleTag(article_id=article.id, tag_id=tag.id)
            article_tags.append(article_tag)
            # 注意：不要同时使用 article.tags.append(tag)，否则会导致重复插入
        
        tag_names = [tag.name for tag in selected_tags]
        print(f"  文章 '{article.title}' 分配标签: {', '.join(tag_names)}")
    
    return article_tags

def generate_comments(articles):
    """生成评论数据"""
    print("生成评论数据...")
    comments = []
    
    for article in articles:
        # 每篇文章生成0-5条评论
        num_comments = random.randint(0, COMMENTS_PER_ARTICLE)
        
        for _ in range(num_comments):
            author_name = random.choice(AUTHOR_NAMES)
            author_email = f"{author_name.lower()}@example.com"
            content = random.choice(COMMENT_TEMPLATES)
            
            # 随机生成评论时间（在文章创建时间之后）
            days_after = random.randint(0, 30)
            created_at = article.created_at + timedelta(days=days_after)
            
            comment = Comment(
                article_id=article.id,
                author_name=author_name,
                author_email=author_email,
                content=content,
                created_at=created_at,
                is_approved=True
            )
            
            comments.append(comment)
        
        if num_comments > 0:
            print(f"  为文章 '{article.title}' 生成 {num_comments} 条评论")
    
    return comments

def clear_existing_data():
    """清空现有数据（可选）"""
    print("清空现有数据...")
    
    # 注意：这会删除所有数据，请谨慎使用
    try:
        # 按正确顺序删除（避免外键约束）
        db.session.query(Comment).delete()
        db.session.query(ArticleTag).delete()
        db.session.query(Tag).delete()
        db.session.query(Article).delete()
        db.session.commit()
        print("  数据已清空")
    except Exception as e:
        db.session.rollback()
        print(f"  清空数据时出错: {e}")

def main():
    """主函数"""
    print("开始生成模拟数据...")
    print("=" * 50)
    
    with app.app_context():
        # 可选：清空现有数据
        clear_existing_data()
        
        # 生成数据
        articles = generate_articles()
        tags = generate_tags()
        
        # 添加到数据库
        print("\n将数据添加到数据库...")
        db.session.add_all(articles)
        db.session.add_all(tags)
        db.session.commit()
        print("  文章和标签已保存")
        
        # 为文章分配标签
        article_tags = assign_tags_to_articles(articles, tags)
        db.session.add_all(article_tags)
        db.session.commit()
        print("  文章标签关系已保存")
        
        # 生成评论
        comments = generate_comments(articles)
        if comments:
            db.session.add_all(comments)
            db.session.commit()
            print("  评论已保存")
        
        # 更新文章的评论计数
        for article in articles:
            article.comment_count = len([c for c in comments if c.article_id == article.id])
        db.session.commit()
        print("  文章评论计数已更新")
        
        # 统计信息
        print("\n" + "=" * 50)
        print("数据生成完成！")
        print(f"  生成文章数: {len(articles)}")
        print(f"  生成标签数: {len(tags)}")
        print(f"  生成评论数: {len(comments)}")
        print(f"  文章-标签关系数: {len(article_tags)}")
        print("\n数据库现在包含测试数据，可以用于开发和测试。")

if __name__ == "__main__":
    # 检查是否在正确的目录中运行
    if not os.path.exists("../../app.py"):
        print("错误：请在包含app.py的目录中运行此脚本")
        print("当前目录:", os.getcwd())
        sys.exit(1)
    
    # 确认操作
    print("警告：此脚本将向数据库插入模拟数据。")
    print("请确保您了解此操作的影响。")
    
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
