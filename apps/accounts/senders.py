from flask_mail import Message
from flask import render_template, current_app
import jwt
from setup.settings import SITE_NAME, DEFAULT_FROM_PHONE, DEFAULT_FROM_EMAIL
from . threads import EmailMessageThread, SmsMessageThread
from . tokens import Token
import random

class Util:
    @staticmethod
    def send_verification_email(request, user):
        current_site = f'{request.scheme}://{request.host}'
        subject = 'Activate your account'
        msg = Message(
                subject=subject,
                sender = DEFAULT_FROM_EMAIL,
                recipients = [user.email]
            )
        msg.html = render_template('accounts/email-activation-message.html', name=user.name, domain=current_site, site_name=SITE_NAME, token=Token.get_activation_token(user), user_id=user.id, sender_email=DEFAULT_FROM_EMAIL)
        EmailMessageThread(current_app._get_current_object(), msg).start()
    
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
                sender = DEFAULT_FROM_EMAIL,
                recipients = [user.email]
            )
        msg.html = render_template('accounts/welcomemessage.html', domain = current_site, name = user.name, site_name = SITE_NAME )
        
        EmailMessageThread(msg).start()