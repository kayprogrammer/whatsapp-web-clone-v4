from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from apps.accounts.models import User

from apps.common.models import TimeStampedUUIDModel

from setup.extensions import db

class Message(TimeStampedUUIDModel):
    __tablename__ = 'message'

    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'))
    receiver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'))

    text = db.Column(db.Text(), nullable=True)

    vn = db.Column(db.String(), nullable=True)
    file = db.Column(db.String(), nullable=True)

    is_read = db.Column(db.Boolean, default=False)

    @hybrid_property
    def sender(self):
        return User.query.filter_by(id=self.sender_id).first()

    @hybrid_property
    def receiver(self):
        return User.query.filter_by(id=self.receiver_id).first()

    def __repr__(self):
        return f"Message by {self.sender_id} to {self.receiver_id} : {self.text}"