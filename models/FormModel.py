from sqlalchemy import Column, String, Integer, DateTime
from app import db
import datetime
import uuid
from models.FormDataModel import FormData
from flask import jsonify
from schema.FormSchema import FormSchema
import uuid

form_schema = FormSchema(strict=True)

# form model
class Form(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))
    unique_id = Column(String(100))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now().time())
    user_id = Column(Integer)

    def __init__(self, name=None, description=None, unique_id=None, created_at=None, updated_at=None, user_id=None):
        self.name = name
        self.description = description
        self.unique_id = unique_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id

    def get(self, user_id):
        forms = Form.query.filter_by(user_id=user_id).all()

        alteredForms = []

        for form in forms:
            record = {
                'id': form.id,
                'name': form.name,
                'description': form.description,
                'created_at': form.created_at,
                'updated_at': form.updated_at,
                'unique_id': form.unique_id,
                'data_items_count': FormData.query.filter_by(form_id=form.id).count()
            }

            alteredForms.append(record)

        return jsonify(alteredForms)

    def create(self, request, user_id):
        name = request.json['name']
        description = request.json['description']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()
        unique_id = uuid.uuid4().hex

        form = Form(name, description, unique_id, created_at, updated_at, user_id)

        db.session.add(form)
        db.session.commit()

        return form_schema.jsonify(form)

    def getOne(self, unique_id):

        form = Form.query.filter_by(unique_id=unique_id, user_id=user_id).first()

        return form_schema.jsonify(form)

<<<<<<< HEAD
    def update(self, unique_id, request, user_id):
        form = Form.query.filter_by(unique_id=unique_id, user_id=user_id).first()
=======
    def update(self, unique_id, request):
        form = Form.query.filter_by(unique_id=unique_id).first()
>>>>>>> 2761bea38a3ce83198864bbc678e1e65ae19f3c4

        name = request.json['name']
        description = request.json['description']

        form.name = name
        form.description = description
        form.updated_at = datetime.datetime.now()

        db.session.commit()

        return form_schema.jsonify(form)
