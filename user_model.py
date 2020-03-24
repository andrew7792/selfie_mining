from config import db, app


# Instagram User data model
class UserInstagram(db.Model):
    __tablename__ = 'users_instagram'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger(), nullable=False, unique=True)
    name = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=False)
    follows = db.Column(db.Integer(), nullable=True, server_default=0)

    def to_dict(self):
        row = {}
        for c in self.__table__.columns:
            row[c.name] = getattr(self, c.name)
        return row

    @staticmethod
    def add_db(raw, image=None):
        obj = UserInstagram()
        for r in raw:
            if r not in ('id', ):
                if r in UserInstagram.__table__.columns:
                    setattr(obj, r, raw[r])

        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def get_by_user_id(user_id):
        obj = UserInstagram.query.filter_by(user_id=user_id).first()
        return obj

    @staticmethod
    def add_if_not_exists(raw):
        user = UserInstagram.get_by_user_id(raw['user_id'])
        if not user:
            user = UserInstagram.add_db(raw)
            return user, False
        return user, True

