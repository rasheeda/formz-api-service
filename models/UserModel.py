from sqlalchemy import Column, String, Integer, DateTime
from app import db
import datetime
import uuid
from passlib.apps import custom_app_context as pwd_context

# form model
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(200))
    password = Column(String(250))
    api_key = Column(String(200))
    timezone = Column(String(200))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())

    def __init__(self, email, password, api_key, timezone, created_at, updated_at):
        self.email = email
        self.password = password
        self.api_key = timezone
        self.timezone = timezone
        self.created_at = created_at
        self.updated_at = updated_at

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
