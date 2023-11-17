""" 
Application Routes
"""
from app import api
from flask import request
from flask_restx import Resource

from app.models.user import User
from app.models.project import Project
from app.models.time_entry import TimeEntry

from app.services.auth import Auth

@api.route('/api/signup')
class Signup(Resource):
    def post(self):
        input_data = request.get_json()
        response = Auth.signup_user(input_data)
        return response, response['code']
    
    
@api.route('/api/login')
class Login(Resource):
    def post(self):
        input_data = request.get_json()
        response = Auth.login_user(input_data)
        return response, response['code']