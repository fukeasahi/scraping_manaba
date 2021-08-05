from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email    = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        print('gooooooooo views.home')
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
      flash('Email does not exist.', category='error')

  return render_template("login.html", boolean = False)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
  if request.method == "POST":
    email           = request.form.get("email")
    first_name       = request.form.get("firstName")
    password1       = request.form.get("password1")
    password2       = request.form.get("password2")
    manaba_user_name  = request.form.get("manabaUserName")
    manaba_password1 = request.form.get("manabaPassword1")
    manaba_password2 = request.form.get("manabaPassword2")
    line_api_token1   = request.form.get("lineApiToken1")
    line_api_token2   = request.form.get("lineApiToken2")

    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exists.', category='error')
    elif len(email) < 4:
      flash("Email must be greater than 4 characyers.", category="error")
    elif len(first_name) < 2:
      flash("First name must be greater than 2 characyers.", category="error")
    elif password1 != password2:
      flash("Passwords don\'t match.", category="error")
    elif len(password1) < 7:
      flash("Passwords must be greater than 7 characyers.", category="error")
    elif len(manaba_user_name) < 7:
      flash("manaba User Name must be greater than 7 characyers.", category="error")
    elif manaba_password1 != manaba_password2:
      flash("manabaPassword don\'t match.", category="error")
    elif len(manaba_password1) < 7:
      flash("manaba Password must be greater than 7 characyers.", category="error")
    elif line_api_token1 != line_api_token2:
      flash("lineApiToken don\'t match.", category="error")
    elif len(line_api_token1) < 7:
      flash("ineApiToken must be greater than 7 characyers.", category="error")
    else:
      new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'),manaba_user_name=manaba_user_name,manaba_password=generate_password_hash(manaba_password1, method='sha256'),line_api_token = generate_password_hash(line_api_token1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.home'))

  return render_template("sign_up.html")
