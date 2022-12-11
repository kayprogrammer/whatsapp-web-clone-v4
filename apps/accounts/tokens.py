from datetime import datetime, timedelta
import jwt
from setup.settings import SECRET_KEY
from . models import User
from setup.extensions import db

class Token:
    def get_activation_token(user):
        return jwt.encode({'activate_user': str(user.id),
                           'exp':    datetime.utcnow() + timedelta(seconds=30)},
                           key=SECRET_KEY, algorithm="HS256")

    def verify_activation_token(token):
        try:
            user_id = jwt.decode(token,
              key=SECRET_KEY, algorithms=["HS256"])['activate_user']

            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            print(e)
            return None
        if user.is_email_verified:
            return None
        print('worked')
        user.is_email_verified = True
        db.session.commit()
        return user

    def get_reset_token(user):
        return jwt.encode({'reset_password': user.id,
                           'exp':    datetime.utcnow() + timedelta(seconds=900)},
                           key=SECRET_KEY)

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