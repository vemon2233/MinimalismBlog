from app import app
from models import db, Project

with app.app_context():
    # 检查projects表是否存在
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    if 'projects' in inspector.get_table_names():
        print('projects表存在')
        columns = inspector.get_columns('projects')
        print('表结构:')
        for column in columns:
            print(f'  {column["name"]}: {column["type"]}')
    else:
        print('projects表不存在')
        
    # 尝试查询一个项目
    try:
        project = Project.query.first()
        if project:
            print(f'找到项目: {project.name}, image_url: {project.image_url}')
        else:
            print('没有找到项目')
    except Exception as e:
        print(f'查询错误: {e}')
