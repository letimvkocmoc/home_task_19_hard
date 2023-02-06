from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, name):
        return self.session.query(User).filter(User.name == name).one_or_none()

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))

        for k, v in user_d.items():
            setattr(user, k, v)

        self.session.add(user)
        self.session.commit()
