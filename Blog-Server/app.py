from flask import Flask
from flask_cors import CORS
from config import Config
from models import db

from apis.article import article_blueprint
from apis.comment import comment_blueprint
from apis.statistic import statistic_blueprint
from apis.other import other_blueprint
from apis.program import program_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 配置CORS
CORS(app, origins=Config.CORS_ORIGINS)

# 注册蓝图
app.register_blueprint(article_blueprint, url_prefix='/article')
app.register_blueprint(comment_blueprint, url_prefix='/comment')
app.register_blueprint(statistic_blueprint, url_prefix='/statistic')
app.register_blueprint(other_blueprint, url_prefix='/other')
app.register_blueprint(program_blueprint, url_prefix='/program')

# 创建数据库表
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
