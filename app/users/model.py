from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_name = db.Column(db.String(45), nullable=False, unique=True)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, login_name, username, password, active=True):
        self.login_name = login_name
        self.username = username
        self.password = password
        self.active = active

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return check_password_hash(hash, password)
