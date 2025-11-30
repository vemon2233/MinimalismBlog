from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from views.home import home_blueprint
from views.articles import articles_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 配置CORS
CORS(app, origins=Config.CORS_ORIGINS)

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(articles_blueprint, url_prefix='/api')

# 创建数据库表
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
