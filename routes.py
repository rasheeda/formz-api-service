from app import app
from models.FormModel import Form
from models.FormDataModel import FormData
from flask import request, jsonify
from app import db
from schema.FormSchema import FormSchema
from schema.FormDataSchema import FormDataSchema
import datetime
from flask_cors import CORS, cross_origin

form_schema = FormSchema(strict=True)
forms_schema = FormSchema(many=True, strict=True)

form_data_schema = FormDataSchema(strict=True)
forms_data_schema = FormDataSchema(many=True, strict=True)


@app.route('/')
def index():
    return '<h2>You can start using the service by making a POST request to /api/forms</h2>'

@app.route('/api/formz', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def forms():

    if request.method == 'GET':
        forms = Form.query.all()

        alteredForms = []

        for form in forms:
            record = {
                'id': form.id,
                'name': form.name,
                'description': form.description,
                'created_at': form.created_at,
                'updated_at': form.updated_at,
                'data_items_count': FormData.query.filter_by(form_id=form.id).count()
            }

            alteredForms.append(record)

        return jsonify(alteredForms)

    if request.method == 'POST':
        # create a new form
        name = request.json['name']
        description = request.json['description']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        form = Form(name, description, created_at, updated_at)

        db.session.add(form)
        db.session.commit()

        return form_schema.jsonify(form)

@app.route('/api/formz/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def forms_item(id):

    form = Form.query.get(id)

    if request.method == 'GET':
        
        return form_schema.jsonify(form)

    if (request.method == 'PUT' or request.method == 'POST'):
        name = request.json['name']
        description = request.json['description']

        form.name = name
        form.description = description
        form.updated_at = datetime.datetime.now()

        db.session.commit()

        return form_schema.jsonify(form)

    if request.method == 'DELETE':
        db.session.delete(form)
        db.session.commit()


@app.route('/api/formz/<form_id>/data', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def forms_data(form_id):

    if request.method == 'GET':
        form_data = FormData.query.filter_by(form_id=form_id).all()

        return forms_data_schema.jsonify(form_data)

    if request.method == 'POST':
        name = request.json['name']
        form_id = form_id
        description = request.json['description']
        data = request.json['data']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        form_data = FormData(form_id, name, description, data, created_at, updated_at)

        db.session.add(form_data)
        db.session.commit()

        return form_data_schema.jsonify(form_data)

@app.route('/api/formz/<form_id>/data/<form_data_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def forms_data_item(form_id, form_data_id):

    if request.method == 'GET':
        form_data_item = FormData.query.filter_by(form_id=form_id, id=form_data_id).first()

        return form_data_schema.jsonify(form_data_item)

@app.route('/api/formz/<form_id>/data/count', methods=['GET'])
@cross_origin(supports_credentials=True)
def forms_data_count(form_id):
    # count number form data items
    countFormData = FormData.query.filter_by(form_id=form_id).count()

    return jsonify(count=countFormData)

