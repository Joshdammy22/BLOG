from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config
from flask_ckeditor import CKEditor
import os



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = "info"
mail = Mail()
ckeditor = CKEditor()

from Models import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    
    with app.app_context():
        db.create_all()

    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.main.routes import main
    from blog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app