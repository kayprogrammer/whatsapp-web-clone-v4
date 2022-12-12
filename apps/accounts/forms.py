from flask_wtf import FlaskForm
from flask import request, session, flash, redirect, url_for

from wtforms import PasswordField, StringField, BooleanField, SelectField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from datetime import datetime
from setup.extensions import db
from . models import User, Otp
from . senders import Util

def validate_password(form, field):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char.isdigit() for char in field.data) or not any(char.isalpha() for char in field.data) or not any(char in special_characters for char in field.data):
        raise ValidationError('Passwords must contain letters, numbers and special characters.')
    if len(field.data) < 8:
        raise ValidationError('Password must contain at least 8 characters')

def validate_phone(form, field):
    user = User.query.filter_by(phone=field.data).first()
    if user:
        raise ValidationError("Email already registered")
def validate_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError("Email already registered")

class RegisterForm(FlaskForm):
    """Register form."""

    name = StringField(
        validators=[
            DataRequired(),
            Length(min=3, max=25),
        ],
        render_kw={'placeholder': 'Name'}
    )
    email = EmailField(
        validators=[DataRequired(), Length(min=6), validate_email],
        render_kw={'placeholder': 'Email address'}
    )

    phone = StringField(
        validators=[
            DataRequired(), 
            Length(max=20),
            Regexp(
                "^\+[0-9]*$",
                message="Phone number must be in this format: +1234567890"
            ),    
            validate_phone
        ],
        render_kw={'placeholder': 'Phone number'}
    )

    tz = SelectField(
        validators=[DataRequired()],
        render_kw={'placeholder': 'Timezone'}
    )

    password = PasswordField(
        validators=[DataRequired(), validate_password],
        render_kw={'placeholder': 'Password'}
    )

    confirm = PasswordField(
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match"),
        ],
        render_kw={'placeholder': 'Confirm password'}
    )

    terms_agreement = BooleanField(
        validators=[DataRequired(),],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    # def validate(self):
    #     """Validate the form."""
    #     initial_validation = super(RegisterForm, self).validate()
    #     if not initial_validation:
    #         return False
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if user:
    #         self.email.errors.append("Email already registered")
    #         return False
    #     user = User.query.filter_by(phone=self.phone.data).first()
    #     if user:
    #         self.phone.errors.append("Phone already registered")
    #         return False
    #     return True

class LoginForm(FlaskForm):
    email_or_phone = StringField(
        validators=[
            DataRequired(),
        ],
    )

    password = PasswordField(
        validators = [DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

class OtpVerificationForm(FlaskForm):
    otp = IntegerField(validators=[DataRequired(),])

    def __init__(self, *args, **kwargs):
        super(OtpVerificationForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(OtpVerificationForm, self).validate()
        if not initial_validation:
            return False
        phone = session.get('phone')
        otp = self.otp.data
        user = User.query.filter_by(phone=phone).first()

        otp_object = Otp.query.filter_by(user_id=user.id, value=otp).first()
        print(otp)
        if not otp_object:
            self.otp.errors.append("Invalid Otp")
            return False
        diff = datetime.utcnow() - otp_object.created_at
        print(f'Now {datetime.utcnow()}')
        print(f'otp {otp_object.created_at}')
        print(f'Diff {diff.total_seconds()}')
        if diff.total_seconds() > 900:
            self.otp.errors.append('Expired Otp')
            return False
        user.is_phone_verified = True
        db.session.commit()
        if user.is_email_verified:
            Util.send_welcome_email(request, user)
        return otp
