from app import app
from models.FormModel import Form
from models.FormDataModel import FormData
from flask import request, jsonify
from app import db
from schema.FormDataSchema import FormDataSchema
import datetime
from flask_cors import CORS, cross_origin
import uuid
from models.UserModel import User
from flask_httpauth import HTTPBasicAuth
from schema.UserSchema import UserSchema
import datetime
from functools import wraps
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models.BlacklistedTokens import BlacklistedTokens
from app import jwt

form_data_schema = FormDataSchema(strict=True)
forms_data_schema = FormDataSchema(many=True, strict=True)

user_schema = UserSchema(strict=True)

auth = HTTPBasicAuth()

@app.route('/')
def index():
    return '<h2>You can start using the service by making a POST request to /api/forms</h2>'

@app.route('/api/formz', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms():

    if check_if_token_in_blacklist() == False:
        return jsonify({'error': 'blacklisted token provided'})

    # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
    current_user = get_jwt_identity()

    if request.method == 'GET':
        return Form.get(Form())

    if request.method == 'POST':

        return Form.create(Form(), request)

@app.route('/api/formz/<unique_id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_item(unique_id):

    if request.method == 'GET':

        return Form.getOne(Form(), unique_id)

    if request.method == 'PUT':
        return Form.update(Form(), unique_id, request)

    if request.method == 'DELETE':
        db.session.delete(form)
        db.session.commit()


@app.route('/api/formz/<form_unique_id>/data', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data(form_unique_id):

    form = Form.query.filter_by(unique_id=form_unique_id).first()

    if request.method == 'GET':
        form_data = FormData.query.filter_by(form_id=form.id).all()

        return forms_data_schema.jsonify(form_data)

    if request.method == 'POST':
        name = request.json['name']
        form_id = form.id
        description = request.json['description']
        data = request.json['data']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        form_data = FormData(form_id, name, description, data, created_at, updated_at)

        db.session.add(form_data)
        db.session.commit()

        return form_data_schema.jsonify(form_data)

@app.route('/api/formz/<form_unique_id>/data/<form_data_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data_item(form_unique_id, form_data_id):

    form = Form.query.filter_by(unique_id=form_unique_id).first()

    if request.method == 'GET':
        form_data_item = FormData.query.filter_by(form_id=form.id, id=form_data_id).first()

        return form_data_schema.jsonify(form_data_item)

@app.route('/api/formz/<form_unique_id>/data/count', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data_count(form_unique_id):
    # count number form data items
    countFormData = FormData.query.filter_by(unique_id=form_unique_id).count()

    return jsonify(count=countFormData)


@app.route('/api/formz/data/graph', methods=['GET'])
@jwt_required
def formz_data_count_graph():
    # get the number of formz data per form and return the results structured like this
    # {
    #   {form_name: "kkkkk", "data_count": 5}
    # }

    if request.method == 'GET':
        formz = Form.query.all()

        graph_data = [];

        for form in formz:
            data = {
                'form_name': form.name,
                'form_data_count': form_data_count(form.id)
            }

            graph_data.append(data)

        return jsonify(graph_data)

@app.route('/api/formz/data/count/graph', methods=['GET'])
@jwt_required
def formz_period_data_count_graph():
    # The number of data posted per day for all forms belonging to user
    # {data:"dddd", data_count:49}
    if request.method == 'GET':
        # formz_data = FormData.query.group_by(FormData.created_at).limit(10).all()
        rows = db.engine.execute("SELECT COUNT(id) as count, CAST(created_at AS DATE) AS date FROM form_data GROUP BY CAST(created_at AS DATE)")
        data = []

        for row in rows:
            record = {
                "count": row.count,
                "date": row.date.strftime("%x")
            }

            data.append(record)

        return jsonify(data)

@app.route('/api/formz/data/count', methods=['GET'])
@jwt_required
def user_formz_data_count():
    if request.method == 'GET':
        # get the total number of forms for a user
        forms_count = Form.query.count();

        return forms_count

def form_data_count(form_id):
    return FormData.query.filter_by(form_id=form_id).count();

@app.route('/api/users/register', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
def register():

    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        user = User(email, password, '', '', datetime.datetime.now(), datetime.datetime.now())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'email': user.email, 'id': user.id})

@app.route('/api/users/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email = email).first()

        if not user or not user.verify_password(password):
            return "false"

        # when authenticated, return a fresh access token and a refresh token
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        # token = jwt.encode({'user': user.id, 'exp': app.config['JWT_ACCESS_TOKEN_EXPIRES'].__str__()}, app.config['JWT_SECRET_KEY'])
        return jsonify({'access_token': access_token,'refresh_token': refresh_token}, 200)

@app.route('/api/users/logout/access', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
def logout():
    if request.method == 'POST':
        try:
            token = get_raw_jwt()['access_token']
            BlacklistedTokens.add(BlacklistedTokens(), token)

            return jsonify({'success': 'token revoked successfully'})

        except:
            return jsonify({'error': 'failure revoking token'})

@app.route('/api/users/logout/refresh', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_refresh_token_required
def logout_refresh():
    if request.method == 'POST':
        try:
            token = get_raw_jwt()['refresh_token']
            BlacklistedTokens.add(BlacklistedTokens(), token)

            return jsonify({'success': 'token revoked successfully'})

        except:
            return jsonify({'error': 'failure revoking token'})


@app.route('/api/users/token/refresh', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_refresh_token_required
def refresh_token():
    if request.method == 'POST':
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return jsonify({'access_token': new_token}, 200)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    token = decrypted_token['token']
    return BlacklistedTokens.isBlackListedToken(token)
