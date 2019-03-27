from sqlalchemy import Column, String, Integer
from app import db

# form model
class Form(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description