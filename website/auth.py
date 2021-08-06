from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

auth = Blueprint('auth', __name__)

@auth.route("/my_page")
@login_required
def show():
    return render_template("show.html", user=current_user)

@auth.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        first_name = request.form.get("firstName")
        manaba_user_name = request.form.get("manabaUserName")
        email = request.form.get("email")

        user = User.query.filter_by(email=email)
        if email != current_user.email and user.count() >= 1:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characyers.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 2 characyers.", category="error")
        elif len(manaba_user_name) < 7:
            flash("manaba User Name must be greater than 7 characyers.",
                  category="error")
        else:
            current_user.first_name = first_name
            current_user.manaba_user_name = manaba_user_name
            current_user.email = email
            current_user.is_active = True if request.form.get(
                "isActive") == "true" else False
            db.session.commit()
            flash('Account updated!', category='success')
            return redirect(url_for('auth.show'))

    return render_template("update.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.show'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        manaba_user_name = request.form.get("manabaUserName")
        manaba_password1 = request.form.get("manabaPassword1")
        manaba_password2 = request.form.get("manabaPassword2")
        line_api_token1 = request.form.get("lineApiToken1")
        line_api_token2 = request.form.get("lineApiToken2")
        is_active = True

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
            flash("manaba User Name must be greater than 7 characyers.",
                  category="error")
        elif manaba_password1 != manaba_password2:
            flash("manabaPassword don\'t match.", category="error")
        elif len(manaba_password1) < 7:
            flash("manaba Password must be greater than 7 characyers.",
                  category="error")
        elif line_api_token1 != line_api_token2:
            flash("lineApiToken don\'t match.", category="error")
        elif len(line_api_token1) < 7:
            flash("ineApiToken must be greater than 7 characyers.", category="error")
        else:
            with open('receiver.pem', 'rb') as f:
                public_pem = f.read()
                public_key = RSA.import_key(public_pem)

            cipher_rsa = PKCS1_OAEP.new(public_key)
            manaba_password = cipher_rsa.encrypt(manaba_password1.encode())
            line_api_token = cipher_rsa.encrypt(line_api_token1.encode())

            new_user = User(email=email, 
                            first_name=first_name, 
                            password=generate_password_hash(password1, method='sha256'), 
                            manaba_user_name=manaba_user_name, 
                            manaba_password=manaba_password, 
                            line_api_token=line_api_token, 
                            is_active=is_active)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
