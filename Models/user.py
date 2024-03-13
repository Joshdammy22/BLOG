from sqlalchemy import Integer, String, MetaData, Table, Column, DateTime
import sqlalchemy as sa
from datetime import datetime
from blog import db
from flask_login import LoginManager, UserMixin
#from itsdangerous import URLSafeSerializer as Serializer
#from itsdangerous import URLSafeSerializer as Serializer
import base64, os
from sqlalchemy.sql import func
from flask import current_app
import time


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    email = sa.Column(sa.String(80), unique=True, nullable=False)
    full_name = sa.Column(sa.String(120))
    bio = sa.Column(sa.Text)
    image_file = sa.Column(sa.String(255), default='images/default.jpg')
    password_hash = sa.Column(sa.String, nullable=False)
    gender = sa.Column(db.String(10))  
    nationality = sa.Column(sa.String(50))  
    date_of_birth = sa.Column(sa.Date)  
    created_at = sa.Column(db.DateTime, default=datetime.utcnow)
    updated_time = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy=True)
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy=True)
    media = db.relationship('Media', backref='user', lazy=True)


    # def generate_confirmation_token(email):
    #     serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    #     return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


    # def confirm_token(token, expiration=3600):
    #     serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    #     try:
    #         email = serializer.loads(
    #         token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
    #         )
    #         return email
    #     except Exception:
    #         return False


    # def generate_confirmation_token(self, expiration=3600):
    #     s = URLSafeSerializer(current_app.config['SECRET_KEY'])
    #     confirmation_payload = {'confirm': self.id}
    #     confirmation_token = s.dumps(confirmation_payload, salt=current_app.config['SECURITY_SALT'])
    #     return confirmation_token

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     db.session.commit()
    #     return True