from app import db
from datetime import datetime

class TimeEntry(db.Model):
    """
    Class TimeEntry
    data model for handling time entry query
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project = db.Column(db.String(120))
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
