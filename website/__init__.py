from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# ここから環境変数の設定
import os
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
RECEIVER_KEY = os.environ.get("RECEIVER_KEY")
# ここまで

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "hjdfajhkfdka dadfsa"
  app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
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
  if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created Database!')