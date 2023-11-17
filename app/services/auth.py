from app import db
from app.models.user import User
from app.schema.signup_user_schema import SignupUserSchema
from app.schema.login_user_schema import LoginUserSchema

from werkzeug.security import generate_password_hash, check_password_hash

class Auth:
    """
    Class that handles the signup and login functions
    """
    def login_user(request):
        login_user_schema = LoginUserSchema()
        errors = login_user_schema.validate(request)
        
        if errors:
            return {'message' : errors, 'code' : 400}

        param = login_user_schema.load(request)
        
        get_user = User.query.filter_by(username = param['username']).first()

        if get_user is None:
            return {'message' : 'User not found', 'code' : 400}
        
        if check_password_hash(get_user.password, param['password']):
            return {'message' : 'Login Successfully', 'code' : 400}
        else:            
            return {'message' : 'Wrong Password', 'code' : 400}
        

    def signup_user(request):        
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
                'code'      : 200, 
                'message'   : 'User created successfully'
            }
        except Exception as e:
            return {
                'code'      : 500,
                'message'   : str(e)
            }