from app import db
from datetime import datetime


class TimeEntry(db.Model):
    """ Class TimeEntry: data model for handling time entry query """

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column('start_time', db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column('end_time', db.DateTime, nullable=True)
    project = db.Column('project', db.String(120))
    description = db.Column('description', db.Text)
    created_at = db.Column('created_at', db.DateTime, default=datetime.utcnow)

    def ordinal(week_number):
        """ Return the ordinal representation of a number """
        if 10 <= week_number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(week_number % 10, 'th')
        return str(week_number) + suffix