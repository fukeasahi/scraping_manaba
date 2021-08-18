from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
import re
import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__, static_folder='./static')
  app.config["SECRET_KEY"] = "hjdfajhkfdka dadfsa"

   # ここからsqliteの記述
  # app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
   # ここまで

  # ここからpostgresql
  uri = os.environ.get('DATABASE_URL')  # or other relevant config var
  if uri.startswith("postgres://"):
      uri = uri.replace("postgres://", "postgresql://", 1)
  conn = psycopg2.connect(uri, sslmode='require')
  app.config["SQLALCHEMY_DATABASE_URI"] = conn
  # ここまで

  db.init_app(app)

  from .views import views
  from .auth import auth
  from .manaba import manaba

  app.register_blueprint(views, url_prefix="/")
  app.register_blueprint(auth,  url_prefix="/")
  app.register_blueprint(manaba,url_prefix="/")

  from .models import User, Note

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app

def create_database(app):
  # ここからsqliteの記述
  # if not path.exists('website/' + DB_NAME):
  #   db.create_all(app=app)
  #   print('Created Database!')
  # ここまで

  # ここからpostgresql
  print('Created Database!')
  # ここまで