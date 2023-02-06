from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthService(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None in [email, password]:
            return "", 401

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        req_json = request.json
        access_token = req_json.get("access_token")
        refresh_token = req_json.get("refresh_token")
        validated = auth_service.validate_tokens((access_token, refresh_token))

        if not validated:
            return 'Invalid token', 400

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 201


@auth_ns.route('/register')
class RegisterViews(Resource):
    def post(self):
        data = request.json

        email = data.get('email')
        password = data.get('password')

        if None in [email, password]:
            return "", 400

        user_service.create(data)

        return "", 201














    