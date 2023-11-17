""" 
Application Routes
"""
from app import api
from flask import request
from flask_restx import Resource

from app.decorators.middleware import required_auth_token

from app.services.auth import AuthService
from app.services.time_entry import TimeEntryService
from app.schema.time_entry_schema import TimeEntrySchema

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
    @required_auth_token
    def post(self):
        """
        Do User time in
        """
        # Validate time entry request parameters
        time_entry_schema = TimeEntrySchema()
        errors = time_entry_schema.validate(request.get_json())                
        if errors:
            return {'message' : errors, 'code' : 400}

        # Validate if user already time in        
        get_auth_token = AuthService.get_auth_user(request)     
        status, time_entry = TimeEntryService.validateTimeEntry(get_auth_token['user'])
        if status == True:
            response =  TimeEntryService.doTimeEntryIn(get_auth_token['user'], request.get_json())
            return response, response['code']
        else:                
            return {'code' : 400, 'message': 'User already timed in for today'}, 400
    
    @required_auth_token
    def put(self):
        """
        Do User time out
        """        
        get_auth_token = AuthService.get_auth_user(request)           
        status, time_entry = TimeEntryService.validateTimeEntry(get_auth_token['user'])
    
        if status == False:
            response =  TimeEntryService.doTimeEntryOut(time_entry)
            return response, response['code']
        else:                
            return {'code' : 400, 'message': 'User already timedout for today'}, 400