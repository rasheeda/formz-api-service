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
from schema.UserSchema import UserSchema
import datetime
from functools import wraps
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models.BlacklistedTokens import BlacklistedTokens
from app import jwt
import secrets

form_data_schema = FormDataSchema(strict=True)
forms_data_schema = FormDataSchema(many=True, strict=True)

user_schema = UserSchema(strict=True)

@app.route('/')
def index():
    return '<h2>You can start using the service by making a POST request to /api/forms</h2>'

@app.route('/api/formz', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms():
    # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
    current_user = get_jwt_identity()

    if request.method == 'GET':
        return Form.get(Form(), current_user)

    if request.method == 'POST':

        return Form.create(Form(), request, current_user)

@app.route('/api/formz/<unique_id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_item(unique_id):

    current_user = get_jwt_identity();

    if request.method == 'GET':

        return Form.getOne(Form(), unique_id, current_user)

    if request.method == 'PUT':
        return Form.update(Form(), unique_id, request, current_user)

    if request.method == 'DELETE':
        form = Form.query.filter_by(unique_id=unique_id, user_id=current_user).first()
        db.session.delete(form)
        db.session.commit()


@app.route('/api/formz/<form_unique_id>/app/data', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data_app(form_unique_id):

    if request.method == 'GET':
        current_user = get_jwt_identity()

        return get_formz_data(form_unique_id, current_user)

@app.route('/api/formz/<form_unique_id>/data', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def forms_data(form_unique_id):

    user = User.query.filter_by(api_key=request.json['api_key']).first();

    if user is None:
        return jsonify({'error': 'invalid api key'}, 404)

    if request.method == 'GET':

        return get_formz_data(form_unique_id, user.id)

    if request.method == 'POST':
        form = Form.query.filter_by(unique_id=form_unique_id, user_id=user.id).first()

        if form is None:
            return jsonify({'error': 'invalid form unique id'}, 404)

        name = request.json['name']
        description = request.json['description']
        data = request.json['data']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()
        form_id = form.id

        form_data = FormData(form_id, name, description, data, created_at, updated_at)

        db.session.add(form_data)
        db.session.commit()

        return form_data_schema.jsonify(form_data)

def get_formz_data(form_unique_id, user_id):
    form_data = (db.session.query(FormData)
    .join(Form).filter(Form.user_id==user_id).filter(Form.unique_id==form_unique_id)
    .all())

    return forms_data_schema.jsonify(form_data)

@app.route('/api/formz/<form_unique_id>/data/<form_data_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data_item(form_unique_id, form_data_id):

    current_user = get_jwt_identity();

    form = Form.query.filter_by(unique_id=form_unique_id, user_id=current_user).first()

    if form:
        if request.method == 'GET':
            form_data_item = FormData.query.filter_by(form_id=form.id, id=form_data_id).first()

            return form_data_schema.jsonify(form_data_item)

    return jsonify({'error': 'invalid user form specified'})

@app.route('/api/formz/<form_unique_id>/data/count', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def forms_data_count(form_unique_id):

    current_user = get_jwt_identity();

    # count number form data items
    countFormData = db.engine.execute("SELECT COUNT(1) FROM form_data JOIN form ON "\
                                  "form_data.form_id = form.id WHERE "\
                                  "form.user_id={} AND form.unique_id='{}'".format(current_user, form_unique_id))

    # countFormData = FormData.query.filter_by(unique_id=form_unique_id).count()

    return jsonify(count=countFormData)

@app.route('/api/formz/data/graph/count', methods=['GET'])
@jwt_required
def formz_data_count_graph():

    current_user = get_jwt_identity();

    if request.method == 'GET':
        formz = Form.query.filter_by(user_id=current_user).all()

        graph_data = [];

        for form in formz:
            data = {
                'form_name': form.name,
                'form_data_count': form_data_count(form.id)
            }

            graph_data.append(data)

        return jsonify(graph_data)

@app.route('/api/formz/data/graph/count/date', methods=['GET'])
@jwt_required
def formz_period_data_count_graph():

    current_user = get_jwt_identity();

    formz = Form.query.filter_by(user_id=current_user).first()

    # The number of data posted per day for all forms belonging to user
    # {data:"dddd", data_count:49}
    if request.method == 'GET':
        # formz_data = FormData.query.group_by(FormData.created_at).limit(10).all()
        rows = db.engine.execute("SELECT COUNT(1) as count, CAST(form_data.created_at AS DATE) AS date"\
                                 " FROM form_data "\
                                 " JOIN form ON form.id = form_data.form_id "\
                                 " WHERE form.id = "+str(formz.id)+" GROUP BY CAST(form_data.created_at AS DATE)")
        data = []

        for row in rows:
            record = {
                "count": row.count,
                "date": row.date.strftime("%x")
            }

            data.append(record)

        return jsonify(data)

@app.route('/api/formz/total/count', methods=['GET'])
@jwt_required
def formz_count():

    current_user = get_jwt_identity();

    if request.method == 'GET':
        forms_count = Form.query.filter_by(user_id=current_user).count();

        return jsonify(forms_count)

@app.route('/api/formz/data/total/count', methods=['GET'])
@jwt_required
def formz_data_count():

    current_user = get_jwt_identity();

    if request.method == 'GET':
        form = Form.query.filter_by(user_id=current_user).first();

        return jsonify(form_data_count(form.id))

def form_data_count(form_id):
    return FormData.query.filter_by(form_id=form_id).count();

@app.route('/api/users/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():

    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        # check if user with the email exists in the database
        user_exists = User.query.filter_by(email = email).first()
        if user_exists:
            return jsonify({'message': 'user email already exists'}), 404

        user = User(email, password, '', '', datetime.datetime.now(), datetime.datetime.now())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200

@app.route('/api/users/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email = email).first()

        if not user or not user.verify_password(password):
            return jsonify({'message': 'invalid login'}), 404

        # when authenticated, return a fresh access token and a refresh token
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        # token = jwt.encode({'user': user.id, 'exp': app.config['JWT_ACCESS_TOKEN_EXPIRES'].__str__()}, app.config['JWT_SECRET_KEY'])
        return jsonify({'access_token': access_token,'refresh_token': refresh_token}), 200

@app.route('/api/users/logout/access', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
def logout():
    if request.method == 'POST':
        try:
            token = get_raw_jwt()['jti']
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
            token = get_raw_jwt()['jti']
            BlacklistedTokens.add(BlacklistedTokens(), token)

            return jsonify({'success': 'token revoked successfully'})

        except:
            return jsonify({'error': 'failure revoking token'})


@app.route('/api/auth/token/refresh', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_refresh_token_required
def refresh_token():
    print(request)
    if request.method == 'POST':
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)

        return jsonify({'access_token': new_token})

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    token = decrypted_token['jti']
    return BlacklistedTokens.isBlackListedToken(token)

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401

@app.route('/api/formz/users/key', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
def get_api_key():
    if request.method == 'GET':
        current_user = get_jwt_identity();

        user = User.query.filter_by(id=current_user).first()

        return jsonify({'api_key': user.api_key})

@app.route('/api/formz/users/key/generate', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
def generate_api_key():
    if request.method == 'POST':
        current_user = get_jwt_identity();
        user = User.query.filter_by(id=current_user).first()

        user.api_key = secrets.token_hex()
        db.session.commit()

        return jsonify({'api_key': user.api_key})
