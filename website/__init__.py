from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
import re
import psycopg2

DB_NAME = "database.db"
db = SQLAlchemy()

def create_app():
  app = Flask(__name__, static_folder='./static')
  app.config["SECRET_KEY"] = "hjdfajhkfdka dadfsa"

  # ここからsqliteの記述
  # app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
  # ここまで

  # ここからpostgresql
  uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flasknote"
  if uri.startswith("postgres://"):
      uri = uri.replace("postgres://", "postgresql://", 1)
  app.config["SQLALCHEMY_DATABASE_URI"] = uri
  # ここまで

  db.init_app(app)

  from .views import views
  from .auth import auth
  from .manaba import manaba

  app.register_blueprint(views, url_prefix="/")
  app.register_blueprint(auth,  url_prefix="/")
  app.register_blueprint(manaba,url_prefix="/")

  from .models import User #,Note

  # ここからsqliteの記述
  # create_database(app)
  # ここまで

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app

# ここからsqliteの記述
# def create_database(app):
#   if not path.exists('website/' + DB_NAME):
#     db.create_all(app=app)
#     print('Created Database!')
# ここまで

