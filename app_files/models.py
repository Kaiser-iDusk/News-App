from app_files import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    country = db.Column(db.String(length=20), nullable=False)
    language = db.Column(db.String(length=20), nullable=False)
    password = db.Column(db.String(length=60), nullable=False)
    technology = db.Column(db.Integer, default=0)
    business = db.Column(db.Integer, default=0)
    entertainment = db.Column(db.Integer, default=0)
    science = db.Column(db.Integer, default=0)
    health = db.Column(db.Integer, default=0)
    sports = db.Column(db.Integer, default=0)

    def check_pwd_correction(self, pwd) -> bool:
        return (self.password == pwd)
    def __repr__(self) -> str:
        return f'ID: {self.id} | Name: {self.username}'