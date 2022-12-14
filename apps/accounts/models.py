from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy.types as types

from setup.extensions import db, bcrypt
from apps.common.models import TimeStampedUUIDModel
from apps.chat.models import Message

from datetime import datetime


from . validators import *
from . choices import *

class Timezone(TimeStampedUUIDModel):
    __tablename__ = 'timezone'
    name = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return '<Timezone %r>' % self.name

from . managers import UserManager, OtpManager # Leave this here cos of some circular imports error

class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        l = [k for k, v in self.choices.items() if v == value]

        if len(l) < 1:
            raise ValueError('Invalid Choice')
        return l[0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

class User(UserManager, TimeStampedUUIDModel, UserMixin):
    name = db.Column(db.String(50))
    email = db.Column(db.String(), unique=True)
    phone = db.Column(db.String(20), unique=True)
    _password = db.Column(db.String())
    tz = db.Column(db.Integer(), db.ForeignKey('timezone.pkid'))
    avatar = db.Column(db.String(), default="https://res.cloudinary.com/kay-development/image/upload/v1667610903/whatsappclonev1/default/Avatar-10_mvq1cm.jpg")
    theme = db.Column(ChoiceType(THEME_CHOICES), default="DARK")
    wallpaper = db.Column(db.String(), default="https://res.cloudinary.com/kay-development/image/upload/v1670371074/whatsappwebclonev4/bg-chat_lrn705.png")
    status = db.Column(db.String(300), default="Hey There! I'm using Whatsapp Web Clone V1!")

    #---Privacy Settings---#
    last_seen = db.Column(ChoiceType(PRIVACYCHOICES.last_seen), default="EVERYONE")
    avatar_status = db.Column(ChoiceType(PRIVACYCHOICES.avatar_status), default="EVERYONE")
    about_status = db.Column(ChoiceType(PRIVACYCHOICES.about_status), default="EVERYONE")
    group_status = db.Column(ChoiceType(PRIVACYCHOICES.groups_status), default="EVERYONE")
    message_timer = db.Column(ChoiceType(PRIVACYCHOICES.message_timer), default="OFF")
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

    current_activation_jwt = db.Column(MutableDict.as_mutable(JSONB), default={'token': "", 'used': False})
    current_password_jwt = db.Column(MutableDict.as_mutable(JSONB), default={'token': "", 'used': False})

    otp = db.relationship("Otp", uselist=False, backref="user", passive_deletes=True)
    terms_agreement = db.Column(db.Boolean, default=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_online = db.Column(db.DateTime, default=datetime.now)

    blockers = db.relationship('BlockedContact', foreign_keys="BlockedContact.blocker_id", backref='blocker_user', lazy=True)
    blockees = db.relationship('BlockedContact', foreign_keys="BlockedContact.blockee_id", backref='blockee_user', lazy=True)

    sender_messages = db.relationship('Message', foreign_keys="Message.sender_id", backref='sender_user', lazy=True, passive_deletes=True)
    receiver_messages = db.relationship('Message', foreign_keys="Message.receiver_id", backref='receiver_user', lazy=True, passive_deletes=True)


    def __repr__(self):
        return self.name

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value).decode('UTF-8')

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password.encode("utf-8"), value)

class Otp(OtpManager, TimeStampedUUIDModel):
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'))
    value = db.Column(db.Integer)

class BlockedContact(TimeStampedUUIDModel):
    blocker_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    blockee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    def __repr__(self):
        try:
            return f"{self.blocker_id} blocked {self.blockee_id}"
        except:
            return "Block issues"    

    __table_args__ = (db.UniqueConstraint('blocker_id', 'blockee_id'), )
