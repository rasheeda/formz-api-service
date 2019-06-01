from sqlalchemy import Column, String, Integer, DateTime
from app import db
import datetime

# form model
class Form(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())

    def __init__(self, name, description, created_at, updated_at):
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at