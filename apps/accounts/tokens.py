from datetime import datetime, timedelta
import jwt
from setup.settings import SECRET_KEY
from . models import User

class Token:
    def get_activation_token(user):
        return jwt.encode({'activate_user': str(user.id),
                           'exp':    datetime.utcnow() + timedelta(minutes=15)},
                           key=SECRET_KEY)

    def verify_activation_token(user_obj, token):
        try:
            user_id = jwt.decode(token,
              key=SECRET_KEY)['activate_user']

            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            print(e)
            return None
        if user_obj.id != user_id:
            return None

        print('worked')
        user.is_email_verified = True
        db.session.commit()
        return user

    def get_reset_token(user):
        return jwt.encode({'reset_password': user.id,
                           'exp':    datetime.utcnow() + timedelta(minutes=15)},
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