from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rianwp2015'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alsxwcywlyqvwn:fc2c745bd8053a8931e92c259a6645982b4e973cbf3f8f864a5fd5300ab755a7@ec2-3-225-79-57.compute-1.amazonaws.com:5432/d7lj1lqhf5kjfu'
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Databarang, Transaksi, Indexintegrity
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Silahkan login untuk mengakses Dashboard"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app



    
