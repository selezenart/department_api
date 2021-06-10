import datetime
from functools import wraps

import jwt
import werkzeug.security
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.services.user_service import UserService

from app import db, app
from app.schemas.users import UsersSchema


class AuthRegister(Resource):
    user_schema = UsersSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': "User with such a email already exists"}
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = UserService.fetch_user_by_username(db.session, username=auth.get('username', ''))
        if not user or not werkzeug.security.check_password_hash(user.password, auth.get('password', '')):
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY']
        )
        return jsonify(
            {
                "token": token
            }
        )


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], ['HS256'])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        user = UserService.fetch_user_by_uuid(db.session, uuid)
        if not user:
            return "", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper
