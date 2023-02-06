from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return UserSchema().dump(user), 201, {'location': f"/users/{user.id}"}


@user_ns.route('/<int:rid>')
class UserView(Resource):
    def get(self, rid):
        r = user_service.get_one(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def patch(self, rid):
        req_json = request.json
        if 'id' not in req_json:
            req_json['id'] = rid

        user_service.update(req_json)
        return "", 204

    def delete(self, rid):
        user_service.delete(rid)
        return "", 204


@user_ns.route('/password')
class UpdateUserPasswordViews(Resource):
    def put(self):
        data = request.json

        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        user = user_service.get_user_by_email(email)

        if user_service.compare_passwords(user.password, old_password):
            user.password = user_service.generate_password_hash(new_password)
            result = UserSchema().dump(user)
            user_service.update(result)
            print('Password updated!')
        else:
            print('Password was not updated!')

        return "", 201
