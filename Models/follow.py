from sqlalchemy import Integer, String, MetaData, Table, Column, DateTime
import sqlalchemy as sa
from blog import db
from datetime import datetime

class Follow(db.Model):
    __tablename__ = 'follows'
    id = sa.Column(sa.Integer, primary_key=True)
    follower_id = sa.Column(sa.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = sa.Column(sa.Integer, db.ForeignKey('users.id'), nullable=False)
