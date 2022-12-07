from sqlalchemy.orm.interfaces import AttributeExtension, InstrumentationManager
from sqlalchemy.orm import ColumnProperty
from setup.main import db
from . validators import *
from . models import Timezone

# class InstallValidatorListeners(InstrumentationManager):
#     def post_configure_attribute(self, class_, key, inst):
#         """Add validators for any attributes that can be validated."""
#         prop = inst.prop
#         # Only interested in simple columns, not relations
#         if isinstance(prop, ColumnProperty) and len(prop.columns) == 1:
#             col = prop.columns[0]
#             # if we have string column with a length, install a length validator
#             if isinstance(col.type, String) and col.type.length:
#                 inst.impl.extensions.insert(0, LengthValidator(col.type.length))

# class LengthValidator(AttributeExtension):
#     def __init__(self, max_length):
#         self.max_length = max_length

#     def set(self, state, value, oldvalue, initiator):
#         if len(value) > self.max_length:
#             raise ValueError(f"{value} must be less than {self.max_length} characters")
#         return value

class UserManager(object):
    @classmethod
    def create_user(cls, **kwargs):
        name = kwargs.pop('name', None)
        email = kwargs.pop('email', None)
        phone = kwargs.pop('phone', None)
        password = kwargs.pop('password', None)
        timezone = kwargs.pop('timezone', None)

        if not name:
            raise ValueError("Users must submit a name")

        if not timezone:
            raise ValueError("Users must submit a timezone")

        validate_email(email)
        validate_phone(phone)
        validate_password(password)
            
        kwargs['is_admin'] = False
        
        try:
            timezone = Timezone.query.get(name=name)
        except:
            raise ValueError('Invalid timezone')

        kwargs['timezone'] = timezone.id
        
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def create_superuser(cls, **kwargs):
        name = kwargs.pop('name', None)
        email = kwargs.pop('email', None)
        phone = kwargs.pop('phone', None)
        password = kwargs.pop('password', None)
        timezone = kwargs.pop('timezone', None)

        if not name:
            raise ValueError("Users must submit a name")

        if not timezone:
            raise ValueError("Users must submit a timezone")

        validate_email(email)
        validate_phone(phone)
        validate_password(password)

        kwargs['is_admin'] = True

        try:
            timezone = Timezone.query.get(name=name)
        except:
            raise ValueError('Invalid timezone')

        kwargs['timezone'] = timezone.id

        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()