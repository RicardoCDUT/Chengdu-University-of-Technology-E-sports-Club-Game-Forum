from flask import Flask, render_template
from config import *
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_avatars import Avatars
from flask_ckeditor import CKEditor
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
avatars = Avatars()
ck = CKEditor()
moment = Moment()

basedir = os.path.abspath(os.path.dirname(__file__))



from apps.views import *

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    avatars.init_app(app)
    ck.init_app(app)
    moment.init_app(app)

    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(global_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(be_index_bp)

    #注册功能报错.
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400
    #我们输入语法格式有误，服务器无法理解咱想表达什么。如果不做修改，刷新再多次也没用。
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403
    #403表示服务器理解了本次请求，但拒绝了你的访问，① 你没有权限访问此网站,② 你被禁止访问此网站.

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error/404.html'), 404
    #①页面被删除或不存在,②网址输入有误,③没插网线或没有联网.

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500
    #如果服务器内部出现错误，无法完成请求.


    return app






login_manager.login_view = 'index_bp.index'
login_manager.login_message = u'Please Login!'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.filter_by(id=user_id).first()
    return user
