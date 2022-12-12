from setup.main import db
from . validators import *
from . models import Timezone

class UserManager(object):
    @classmethod
    def create_user(cls, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        password = kwargs.get('password')
        tz = kwargs.get('tz')

        if not name:
            raise ValueError("Users must submit a name")

        if not tz:
            raise ValueError("Users must submit a timezone")
        
        validate_email(email)
        validate_phone(phone)
        validate_password(password)
            
        timezone = Timezone.query.filter_by(name=tz).first()
        if not timezone:
            raise ValueError('Invalid Timezone')

        kwargs['tz'] = timezone.pkid
        kwargs['is_admin'] = False
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def create_superuser(cls, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        password = kwargs.get('password')
        tz = kwargs.get('tz')

        if not name:
            raise ValueError("Users must submit a name")

        if not tz:
            raise ValueError("Users must submit a timezone")
        
        validate_email(email)
        validate_phone(phone)
        validate_password(password)
            
        timezone = Timezone.query.filter_by(name=tz).first()
        if not timezone:
            raise ValueError('Invalid Timezone')

        kwargs['tz'] = timezone.pkid
        kwargs['is_admin'] = True
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

class OtpManager(object):
    @classmethod
    def get_or_create(cls, **kwargs):
        instance = cls.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance