from datetime import datetime

from app import db
from app.models.time_entry import TimeEntry

class TimeEntryService:
    """
    Handles the time-in and time-out entries
    """
    def doTimeEntryIn(request, auth_user):
        """
        Create time entry for user
        """
        auth_user['start_time'] = datetime.utcnow().isoformat()
        time_in_entry = TimeEntry(user_id=auth_user['id'], start_time=datetime.utcnow())

        db.session.add(time_in_entry)

        try:
            db.session.commit()
            return {'code' : 200, 'message' : 'Time Registered Successfully', 'data' : auth_user}
        except Exception as e:
            return {'code' : 400, 'message' : str(e)}


    def doTimeEntryOut():
        pass

    def validateTimeEntry(auth_user):
        """
        Validate if the user has already a Time Entry for today
        """
        today = datetime.utcnow().date()
        start_of_today = datetime.combine(today, datetime.min.time())
        ongoing_entry = TimeEntry.query.filter(
            TimeEntry.user_id == auth_user['id'],
            TimeEntry.end_time.is_(None),
            TimeEntry.start_time >= start_of_today
        ).order_by(TimeEntry.start_time.desc()).first()

        if ongoing_entry:
            """
            User already has time entry
            """
            return False
        else: 
            """
            User already has no time entry
            """
            return True