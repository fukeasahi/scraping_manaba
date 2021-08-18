from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(10000))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
  __tablename__ = 'Users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  line_api_token = db.Column(db.String(150))
  manaba_user_name = db.Column(db.String(150))
  manaba_password = db.Column(db.String(150))
  is_active = db.Column(db.Boolean)
  # date = db.Column(db.DateTime(timezone=True), default=func.now())
  notes = db.relationship('Note')
