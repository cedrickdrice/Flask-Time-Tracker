import jwt
import datetime

from config import Config

from app import db
from app.models.user import User
from app.schema.signup_user_schema import SignupUserSchema
from app.schema.login_user_schema import LoginUserSchema

from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    """
    Class that handles the signup and login functions
    """
    @staticmethod
    def login_user(request):
        """
        Function for logging in user and creating access token
        
        Validates the user credentials against the database. If authentication
        is successful, it generates and returns a JWT access token.

        :param request: request from api request
        :return: A response with status code, message, and data
        """
        login_user_schema = LoginUserSchema()
        errors = login_user_schema.validate(request)
        
        if errors:
            return {'message' : errors, 'code' : 400}

        param = login_user_schema.load(request)
        
        auth_user = User.query.filter_by(username = param['username']).first()

        if auth_user is None:
            return {'message' : 'User not found', 'code' : 400}
        
        if check_password_hash(auth_user.password, param['password']):
            # generate token
            access_token = jwt.encode({
                        'id': auth_user.id,
                        'email': auth_user.email,
                        'username': auth_user.username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1) # 24hrs token life
                    }, Config.SECRET_KEY)
            
            # add access token to response
            param['access_token'] = access_token

            return {'code' : 200, 'message' : 'Login Successfully', 'data' : param}
        else:            
            return {'code' : 400, 'message' : 'Wrong Password'}
        
    @staticmethod        
    def signup_user(request):        
        """
        Function for creating user through signup

        Validates the signup request against the schema and ensures that the
        username and email are not already in use. If validation is successful,
        it creates a new user in the database.

        :param request: request from api request
        :return: A response with status code, message, and data
        """
        signup_user_schema = SignupUserSchema()
        errors = signup_user_schema.validate(request)
        
        if errors:
            return {'message' : errors}

        param = signup_user_schema.load(request)

        get_existing_username = User.query.filter_by(username = param['username']).first()        
        get_existing_email = User.query.filter_by(email = param['email']).first()

        if get_existing_username:
            return {
                'code'      : 400, 
                'message'   : 'Username already exist'
            }
        
        if get_existing_email:
            return {
                'code'      : 400,
                'message'   : 'Email already exist'
            }
        
        hashed_password = generate_password_hash(param['password'])
        
        db.session.add(User(
            username=param['username'],
            email=param['email'],
            password=hashed_password
        ))

        try:
            db.session.commit()
            return {
                'code'      : 201, 
                'message'   : 'User created successfully'
            }
        except Exception as e:
            return {
                'code'      : 500,
                'message'   : str(e)
            }
    @staticmethod        
    def get_auth_user(request):        
        """
        Get auth user from access token

        Decodes the JWT access token from the request headers and retrieves the user's
        information if the token is valid.

        :param request: request from api request
        :return: A response with status code, message, and data
        """
        auth_header = request.headers.get('Authorization')

        # validate if bearer token exist
        auth_content = auth_header.split() if auth_header else []
        access_token = auth_content[1]            
        try:
            # Decode to get the auth user
            decode_auth = jwt.decode(
                access_token,
                Config.SECRET_KEY,
                algorithms="HS256",
                options={"require": ["exp"]}
            )

            return {
                'status'    : True,
                'message'   : 'Valid access token',
                'user'      :  decode_auth
            }
        except:
            return {
                'status'    : False,
                'message'   : 'Failed to decode token'
            }
            
        


