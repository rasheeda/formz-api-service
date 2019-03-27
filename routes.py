from app import app
from models.FormModel import Form
from models.FormDataModel import FormData
from flask import request, jsonify
from app import db
from schema.FormSchema import FormSchema
from schema.FormDataSchema import FormDataSchema
import datetime

form_schema = FormSchema(strict=True)
forms_schema = FormSchema(many=True, strict=True)

form_data_schema = FormDataSchema(strict=True)
forms_data_schema = FormDataSchema(many=True, strict=True)


@app.route('/')
def index():
    return '<h2>You can start using the service by making a POST request to /api/forms</h2>'

@app.route('/api/forms', methods=['POST'])
def forms():
    # create a new form
    name = request.json['name']
    description = request.json['description']

    form = Form(name, description)

    db.session.add(form)
    db.session.commit()

    return form_schema.jsonify(form)

@app.route('/api/forms/<id>', methods=['GET', 'PUT'])
def forms_item(id):
    if request.method == 'GET':
        form = Form.query.get(id)
        return form_schema.jsonify(form)

    if request.method == 'PUT':
        name = request.json['name']
        description = request.json['description']

        form = Form.query.get(id)
        form.name = name
        form.description = description

        db.session.commit()

        return form_schema.jsonify(form)

@app.route('/api/forms/<form_id>/data', methods=['GET', 'POST'])
def forms_data(form_id):

    if request.method == 'GET':
        form_data = FormData.query.filter_by(form_id=form_id).all()

        return forms_data_schema.jsonify(form_data)

    if request.method == 'POST':
        name = request.json['name']
        form_id = request.json['form_id']
        description = request.json['description']
        data = request.json['data']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        form_data = FormData(form_id, name, description, data, created_at, updated_at)

        db.session.add(form_data)
        db.session.commit()

        return form_data_schema.jsonify(form_data)

@app.route('/api/forms/<form_id>/data/<form_data_id>', methods=['GET'])
def forms_data_item(form_id, form_data_id):
    
    if request.method == 'GET':
        form_data_item = FormData.query.filter_by(form_id=form_id, id=form_data_id).first()

        return form_data_schema.jsonify(form_data_item)