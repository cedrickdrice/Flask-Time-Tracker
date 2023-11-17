from datetime import datetime, timedelta

from app import db
from app.models.time_entry import TimeEntry
from app.models.project import Project

from sqlalchemy import func  # added
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
        
    @staticmethod
    def getWeekWorkSummary(auth_user):
        """
        Create summary report of user working hours on project
        
        :param auth_user: current authenticated user
        :return: return dict that contain summary working hours
        """
        today = datetime.utcnow()
        start_of_week = today - timedelta(days=(today.weekday() + 1) % 7)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

        work_summary = db.session.query(
            Project.name,
            func.round(
                func.sum(
                    func.strftime('%s', TimeEntry.end_time) - 
                    func.strftime('%s', TimeEntry.start_time)
                ) / 3600, 2
            ).label('total_hours')
        ).join(
            Project, Project.id == TimeEntry.project
        ).filter(
            TimeEntry.user_id == auth_user['user']['id'],
            TimeEntry.start_time >= start_of_week,
            TimeEntry.end_time <= end_of_week
        ).group_by(
            Project.name
        ).all()

        result = [{
            'project': entry.name,
            'total_hours': entry.total_hours
        } for entry in work_summary]

        week_number = start_of_week.isocalendar()[1]
        ordinal_week = TimeEntry.ordinal(week_number)
        message = f'User Week Summary for the {ordinal_week} week: {start_of_week.strftime("%Y-%m-%d")}'

        return {'code': 200, 'message': message, 'data' : result}