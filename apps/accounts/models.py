from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy_utils.types.choice import ChoiceType
from setup.main import db
from common.models import TimeStampedUUIDModel

from datetime import datetime
from . validators import *
from . managers import UserManager
import uuid

class Timezone(TimeStampedUUIDModel):
    __tablename__ = 'timezone'
    name = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return '<Timezone %r>' % self.name

class PRIVACYCHOICES:
    last_seen = (
        ('EVERYONE', 'EVERYONE'),
        ('MY CONTACTS', 'MY CONTACTS'),
        ('NOBODY', 'NOBODY')
    )

    avatar_status = last_seen
    about_status = last_seen
    groups_status = last_seen

    message_timer = (
        ('24 HOURS', '24 HOURS'),
        ('7 DAYS', '7 DAYS'),
        ('90 DAYS', '90 DAYS'),
        ('OFF', 'OFF')
    )

THEME_CHOICES = (
    ('LIGHT', 'LIGHT'),
    ('DARK', 'DARK'),
    ('SYSTEM_DEFAULT', 'SYSTEM_DEFAULT')
)

class User(UserManager, db.Model):
    pkid = db.Column(db.Integer, primary_key=True)
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    
    name = db.Column(db.String(50))
    email = db.Column(db.String(), unique=True)
    phone = db.Column(db.String(20), unique=True)
    tz = owner = db.Column(db.Integer(), db.ForeignKey('timezone.pkid'))
    avatar = db.Column(db.String(), default="https://res.cloudinary.com/kay-development/image/upload/v1667610903/whatsappclonev1/default/Avatar-10_mvq1cm.jpg")
    theme = db.Column(ChoiceType(THEME_CHOICES), db.String, default="DARK")
    wallpaper = db.Column(db.String(), default="https://res.cloudinary.com/kay-development/image/upload/v1670371074/whatsappwebclonev4/bg-chat_lrn705.png")
    status = db.Column(db.String(300), default="Hey There! I'm using Whatsapp Web Clone V1!")

    #---Privacy Settings---#
    last_seen = db.Column(ChoiceType(PRIVACYCHOICES.last_seen), db.String(), default="EVERYONE")
    avatar_status = db.Column(ChoiceType(PRIVACYCHOICES.avatar_status), db.String(), default="EVERYONE")
    about_status = db.Column(ChoiceType(PRIVACYCHOICES.about_status), db.String(), default="EVERYONE")
    group_status = db.Column(ChoiceType(PRIVACYCHOICES.groups_status), db.String(), default="EVERYONE")
    message_timer = db.Column(ChoiceType(PRIVACYCHOICES.message_timer), db.String(), default="OFF")
    read_receipts = db.Column(db.Boolean, default=True)
    blocked_contacts_count = db.Column(db.Integer, default="0")
    #----------------------#

    #---Notification Settings---#
    message_notifications = db.Column(db.Boolean, default=True)
    show_previews = db.Column(db.Boolean, default=True)
    show_reaction_notifications = db.Column(db.Boolean, default=True)
    sounds = db.Column(db.Boolean, default=True)
    security_notifications = db.Column(db.Boolean, default=True)
    #----------------------#

    otp = db.relationship("Child", uselist=False, backref="user", nullable=True)
    terms_agreement = db.Column(db.Boolean, default=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_online = db.Column(db.DateTime, default=datetime.now)
    date_joined = db.Column(db.DateTime, default=datetime.now)

    blocked_contacts = db.relationship('BlockedContact', backref='user', lazy=True)

    def __repr__(self):
        return self.name


class Otp(TimeStampedUUIDModel):
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    value = db.Column(db.Integer)

class BlockedContact(TimeStampedUUIDModel):
    blocker = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    blockee = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    def __repr__(self):
        try:
            return f"{self.blocker.name} blocked {self.blockee.name}"
        except:
            return "Block issues"    

    __table_args__ = (db.UniqueConstraint('blocker', 'blockee'), )
