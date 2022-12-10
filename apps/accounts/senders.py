from flask_mail import Message
from flask import render_template
import jwt
from setup.settings import MAIL_USERNAME, SITE_NAME, DEFAULT_FROM_PHONE, SECRET_KEY, client
from setup.extensions import mail, db
from . models import User
from datetime import datetime, timedelta
import random
import threading

class Token:
    def get_activation_token(user):
        return jwt.encode({'activate_user': user.id,
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

class EmailMessageThread(threading.Thread):

    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        mail.send(self.msg)

class SmsMessageThread(threading.Thread):

    def __init__(self, body, from_, to):
        self.body = body
        self.from_ = from_
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        client.messages.create(
            body = self.body,
            from_ = self.from_,
            to = self.to
        )

class Util:
    @staticmethod
    def send_verification_email(request, user):
        current_site = f'{request.scheme}://{request.host}'
        subject = 'Activate your account'
        msg = Message(
                        subject=subject,
                        sender = MAIL_USERNAME,
                        recipients = [user.email]
                    )
        msg.html = render_template('accounts/email-activation-message.html', name=user.name, domain=current_site, site_name=SITE_NAME, token=Token.get_activation_token(user), email=user.email)
        EmailMessageThread(msg).start()
    
    @staticmethod
    def send_sms_otp(user):
        code = random.randint(100000, 999999)
        from . models import Otp 
        Otp.get_or_create(user_id=user.id)
        
        body = f'Hello {user.name}! \nYour Phone Verification OTP from {SITE_NAME} is {code} \nExpires in 15 minutes',
        from_ = DEFAULT_FROM_PHONE,
        to = user.phone

        SmsMessageThread(body, from_, to).start()

    @staticmethod
    def send_welcome_email(request, user):
        current_site = f'{request.scheme}://{request.host}'
        subject = 'Account Verified'
        msg = Message(
                        subject=subject,
                        sender = MAIL_USERNAME,
                        recipients = [user.email]
                    )
        msg.html = render_template('accounts/welcomemessage.html', domain = current_site, name = user.name, site_name = SITE_NAME )
        
        EmailMessageThread(msg).start()