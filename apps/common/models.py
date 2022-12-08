from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime
db = SQLAlchemy()
class TimeStampedUUIDModel(db.Model):
    __abstract__ = True
    pkid = db.Column(db.Integer, primary_key=True)
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
