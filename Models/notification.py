from sqlalchemy import Integer, String, MetaData, Table, Column, DateTime
import sqlalchemy as sa
from blog import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, db.ForeignKey('users.id'), nullable=False)
