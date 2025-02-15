from flask import Flask
from .extensions import db, migrate, login_manager, assets
from .config import Config
from .routes.post import post
from .routes.user import user
from .bundles import bundles, register_bundles

def create_app(config_class = Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    app.register_blueprint(user)
    app.register_blueprint(post)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    assets.init_app(app)

    #LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = "Вы не можете получить доступ к данной странице. Нужно сначала войти"
    login_manager.login_message_category = "info"

    #ASSETS
    register_bundles(assets, bundles)

    with app.app_context():
        db.create_all()

    return app