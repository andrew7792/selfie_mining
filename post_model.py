from config import db, app


# Instagram Post data model
class PostInstagram(db.Model):
    __tablename__ = 'posts_instagram'
    id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger(), nullable=True, unique=True)
    user_id = db.Column(db.BigInteger(), nullable=True, unique=False)
    post_time = db.Column(db.DateTime, nullable=True)
    post_likes = db.Column(db.Integer(), nullable=True, server_default=0)
    post_comments = db.Column(db.Integer(), nullable=True, server_default=0)
    post_caption = db.Column(db.UnicodeText(), nullable=True)
    post_image = db.Column(db.UnicodeText(), nullable=True)

    IMAGES_FOLDER_PATH = app.config['IMAGES_FOLDER']


    def to_dict(self):
        row = {}
        for c in self.__table__.columns:
            row[c.name] = getattr(self, c.name)
        return row

    @staticmethod
    def add_db(raw, image=None):
        obj = PostInstagram()
        for r in raw:
            if r not in ('id', 'post_image', ):
                if r in PostInstagram.__table__.columns:
                    setattr(obj, r, raw[r])

        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def create_image_path():
        pass

    @staticmethod
    def create_image_filename():
        pass

    @staticmethod
    def add_image():
        pass




