# decorators.py
from functools import wraps
import jwt

from config import Config
from flask import request
from flask import app
from app.models.user import User

def required_auth_token(f):
    """
    Validate if access token exist, invalid or valid as middleware
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        # validate if bearer token exist
        auth_content = auth_header.split() if auth_header else []
        valid_token = True if (len(auth_content) == 2 and auth_content[0] == 'Bearer') else False
        
        if valid_token == False:
            return {
                'code'    : 400,
                'message'   : 'Invalid request. Missing access token'
            }

        access_token = auth_content[1]            
        try:
            # Decode to get the auth user
            decode_auth = jwt.decode(
                access_token,
                Config.SECRET_KEY,
                algorithms="HS256",
                options={"require": ["exp"]}
            )

            auth_user = User.query.filter_by(id = decode_auth['id']).first()
            if auth_user is None:
                return {
                    'code'    : 400,
                    'message'   : 'Invalid access token. Unauthorized'
                }, 401

            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return {
                'code'    : 400,
                'message'   : 'Expired access token'
            }
        except jwt.InvalidTokenError:
            return {
                'code'    : 400,
                'message'   : 'Invalid access token'
            }

    return decorator