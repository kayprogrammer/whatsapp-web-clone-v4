from sqlalchemy.dialects.postgresql import UUID
# from apps.accounts.models import User

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

    def __repr__(self):
        return f"Message by {self.sender_id} to {self.receiver_id} : {self.text}"