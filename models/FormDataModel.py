from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
import datetime
from app import db


# form data model
class FormData(db.Model):
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())

    
    def __init__(self, form_id=None, name=None, description=None, data=None, created_at=None, updated_at=None):
        self.form_id = form_id
        self.name = name
        self.description = description
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at