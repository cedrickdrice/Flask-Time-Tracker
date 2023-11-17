from app import db
from datetime import datetime

class Project(db.Model):
    """ Class Project: data model for handling project query """

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(120), nullable=False)
    description = db.Column('description', db.Text, nullable=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow)