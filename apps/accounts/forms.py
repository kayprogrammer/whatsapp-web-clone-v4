from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, BooleanField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from . models import User

def validate_password(form, field):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char.isdigit() for char in field.data) or not any(char.isalpha() for char in field.data) or not any(char in special_characters for char in field.data):
        raise ValidationError('Passwords must contain letters, numbers and special characters.')
    if len(field.data) < 8:
        raise ValidationError('Password must contain at least 8 characters')

class RegisterForm(FlaskForm):
    """Register form."""

    name = StringField(
        validators=[
            DataRequired(),
            Length(min=3, max=25),
        ],
    )
    email = EmailField(
        validators=[DataRequired(), Length(min=6)],
    )

    phone = StringField(
        validators=[
            DataRequired(), 
            Length(max=20),
            Regexp(
                "^\+[0-9]*$",
                message="Phone number must be in this format: +1234567890"
            ),    
        ],
    )

    tz = SelectField(
        validators=[DataRequired()],
    )

    password = PasswordField(
        validators=[DataRequired(), validate_password]
    )

    confirm = PasswordField(
        [
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    terms_agreement = BooleanField(
        validators=[DataRequired(),],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        user = User.query.filter_by(phone=self.phone.data).first()
        if user:
            self.email.errors.append("Phone already registered")
            return False
        return True

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