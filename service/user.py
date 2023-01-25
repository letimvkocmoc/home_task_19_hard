import hashlib
import base64
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_d):
        user_d["password"] = self.generate_password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.generate_password_hash(user_d.get("password"))
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    def generate_password_hash(self, password):
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hashed_password)

    def compare_passwords(self, password_hashed, password) -> bool:
        return hmac.compare_digest(
            base64.b64encode(password_hashed),
            hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )
