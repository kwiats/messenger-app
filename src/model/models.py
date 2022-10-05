from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    picture_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<User %r %s %d>' % self.firstname, self.lastname, self.email
    
