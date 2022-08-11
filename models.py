from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime
db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    post_code = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<user {self.id} {self.username}'
    
    def serialize(self):
        return {
            'id':self.id,
            'username':self.username,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'address': self.address,
            'city':self.city,
            'country': self.country,
            'post_code': self.post_code,
            'is_admin':self.is_admin,
            'api_key':self.api_key,
            'is_active':self.is_active,
            'password':self.password
        }

    def update_api_key(self):
        self.api_key = generate_password_hash(self.username+str(datetime.utcnow))