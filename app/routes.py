from app import api
from flask import jsonify
from flask_restx import Resource

@api.route('/api/welcome')
class Welcome(Resource):
    def get(self):        
        return jsonify({'message': 'welcome'})