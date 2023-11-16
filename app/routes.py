from flask import jsonify
from flask_restx import Resource
from app import api

@api.route('/api/welcome')  # If using a namespace, replace 'api' with 'ns'
class Welcome(Resource):
    def get(self):        
        return jsonify({'message': 'welcome'})