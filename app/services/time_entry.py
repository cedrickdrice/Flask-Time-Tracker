from datetime import datetime

from app import db
from app.models.time_entry import TimeEntry

class TimeEntryService:
    """
    Handles the time-in and time-out entries
    """

    @staticmethod
    def doTimeEntryIn(auth_user, request):
        """
        Create time entry for user

        :param auth_user: current authenticated user
        :return: A response with status code and message, and data
        """
        
        time_in_entry = TimeEntry(
            user_id=auth_user['id'], 
            project=request['project'], 
            description=request['description'], 
            start_time=datetime.utcnow()
        )
        
        db.session.add(time_in_entry)

        try:
            db.session.commit()
            return {'code': 200, 'message': 'Time Registered Successfully', 'data': auth_user}
        except Exception as e:
            return {'code': 400, 'message': str(e)}

    @staticmethod
    def doTimeEntryOut(time_entry):
        """
        Updates the end_time of a user's time entry to record time-out

        :param time_entry: current user time entry
        :return: response with status code and message.
        """
        
        time_entry.end_time = datetime.utcnow()
        try:
            db.session.commit()
            return {'code': 200, 'message': 'Timeout Registered Successfully'}
        except Exception as e:
            return {'code': 400, 'message': str(e)}

    @staticmethod
    def validateTimeEntry(auth_user):
        """
        Validate if the user has already a Time Entry for today

        :param auth_user: current authenticated user
        :return: return boolean indicate if current has user already timed in or no time entry yet
        """
        today = datetime.utcnow().date()
        start_of_today = datetime.combine(today, datetime.min.time())
        ongoing_entry = TimeEntry.query.filter(
            TimeEntry.user_id == auth_user['id'],
            TimeEntry.end_time.is_(None),
            TimeEntry.start_time >= start_of_today
        ).order_by(TimeEntry.start_time.desc()).first()

        if ongoing_entry:
            # User already has time entry
            return False, ongoing_entry
        else: 
            # User already has no time entry
            return True, []