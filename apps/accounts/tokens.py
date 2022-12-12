from flask import session
from datetime import datetime, timedelta
import jwt
from setup.settings import SECRET_KEY
from . models import User
from setup.extensions import db

class Token:
    def get_activation_token(user):
        token = jwt.encode({'activate_user': str(user.id), 'exp':datetime.utcnow() + timedelta(seconds=900)}, key=SECRET_KEY, algorithm="HS256") 
        user.current_activation_jwt = token
        db.session.commit()
        return token

    def verify_activation_token(token):
        try:
            user_id = jwt.decode(token,
              key=SECRET_KEY, algorithms=["HS256"])['activate_user']

            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            return None
        
        if token != user.current_activation_jwt: # Just to invalidate old tokens that are yet to expire
            return None
        if user.is_email_verified:
            return None

        user.is_email_verified = True
        db.session.commit()
        return user

    def get_reset_token(user):
        token = jwt.encode({'reset_password': user.id,
                           'exp': datetime.utcnow() + timedelta(seconds=900)},
                           key=SECRET_KEY)
        user.current_activation_jwt = token
        db.session.commit()
        return token

    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token,
              key=SECRET_KEY)['reset_password']

            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            print(e)
            return
        print('worked')
        return user