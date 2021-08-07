from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
def home():
  return render_template("home.html", user=current_user)

@views.route("/line_api")
def line_api():
  return render_template("line_api.html", user=current_user)