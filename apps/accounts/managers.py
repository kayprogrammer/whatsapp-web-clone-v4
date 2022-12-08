from setup.main import db
from . validators import *
from . models import Timezone

class UserManager(object):
    @classmethod
    def create_user(cls, **kwargs):
        name = kwargs.pop('name', None)
        email = kwargs.pop('email', None)
        phone = kwargs.pop('phone', None)
        _password = kwargs.pop('_password', None)
        timezone = kwargs.pop('timezone', None)

        if not name:
            raise ValueError("Users must submit a name")

        if not timezone:
            raise ValueError("Users must submit a timezone")

        validate_email(email)
        validate_phone(phone)
        validate_password(_password)
            
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
        _password = kwargs.pop('_password', None)
        timezone = kwargs.pop('timezone', None)

        if not name:
            raise ValueError("Users must submit a name")

        if not timezone:
            raise ValueError("Users must submit a timezone")

        validate_email(email)
        validate_phone(phone)
        validate_password(_password)

        kwargs['is_admin'] = True

        try:
            timezone = Timezone.query.get(name=name)
        except:
            raise ValueError('Invalid timezone')

        kwargs['timezone'] = timezone.id

        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()