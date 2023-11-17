""" 
Application Routes
"""
from app import api
from flask import request
from flask_restx import Resource

from app.models.user import User
from app.models.project import Project

from app.services.auth import AuthService
from app.services.time_entry import TimeEntryService

@api.route('/api/signup')
class Signup(Resource):
    """
    Signup user to application
    """
    def post(self):
        input_data = request.get_json()
        response = AuthService.signup_user(input_data)
        return response, response['code']
    
    
@api.route('/api/login')
class Login(Resource):
    """
    Authenticate user and return access token
    """
    def post(self):
        input_data = request.get_json()
        response = AuthService.login_user(input_data)
        return response, response['code']
        
@api.route('/api/time')
class TimeEntry(Resource):
    def post(self):
        """
        Do User time in
        """
        get_auth_token = AuthService.validate_access_token(request)            
        
        if get_auth_token['status'] == True:
            status, time_entry = TimeEntryService.validateTimeEntry(get_auth_token['user'])
            if status == True:
                response =  TimeEntryService.doTimeEntryIn(request, get_auth_token['user'])
                return response, response['code']
            else:                
                return {'code' : 400, 'message': 'User already timed in for today'}, 400

        else:
            return {'message': get_auth_token['message']}, 500
    
    def put(self):
        """
        Do User time out
        """        
        get_auth_token = AuthService.validate_access_token(request)                    
        if get_auth_token['status'] == True:
            status, time_entry = TimeEntryService.validateTimeEntry(get_auth_token['user'])
        
            if status == False:
                response =  TimeEntryService.doTimeEntryOut(time_entry)
                return response, response['code']
            else:                
                return {'code' : 400, 'message': 'User already timedout for today'}, 400
        else:
            return {'message': get_auth_token['message']}, 500