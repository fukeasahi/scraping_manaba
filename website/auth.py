from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from cryptography.fernet import Fernet

import os

auth = Blueprint('auth', __name__)

@auth.route("/my_page", methods=["GET", "POST"])
@login_required
def show():
    if request.method == "POST":
        current_user.is_active = True if request.form.get("isActive") == "true" else False
        db.session.commit()
        flash('Account updated!', category='success')
        return redirect(url_for('auth.show'))

    return render_template("show.html", user=current_user)

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
        manaba_user_name1 = request.form.get("manabaUserName1")
        manaba_user_name2 = request.form.get("manabaUserName2")
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
        elif manaba_user_name1 != manaba_user_name2:
            flash("manabaPassword don\'t match.", category="error")
        elif len(manaba_user_name1) < 7:
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
            # ここから暗号化

            # 本番
            f_manaba_user_id=Fernet(os.environ['MANABA_USER_ID_KEY'].encode(encoding='utf-8'))
            f_manaba_password=Fernet(os.environ['MANABA_PASSWORD_KEY'].encode(encoding='utf-8'))
            f_line_api=Fernet(os.environ['LINE_API_KEY'].encode(encoding='utf-8'))

            manaba_user_name=f_manaba_user_id.encrypt(manaba_user_name1.encode())
            manaba_password=f_manaba_password.encrypt(manaba_password1.encode())
            line_api_token=f_line_api.encrypt(line_api_token1.encode())

            manaba_user_name=manaba_user_name.decode('utf-8')
            manaba_password=manaba_password.decode('utf-8')
            line_api_token=line_api_token.decode('utf-8')
            # ここまで暗号化
            print("aaaaaaaaaaaaa")
            new_user = User(email=email, 
                            first_name=first_name, 
                            password=generate_password_hash(password1, method='sha256'), 
                            manaba_user_name=manaba_user_name, 
                            manaba_password=manaba_password, 
                            line_api_token=line_api_token, 
                            is_active=is_active)
            print("bbbbbbbbbbbbbbb")
            db.session.add(new_user)
            print("ccccccccccccccc")
            db.session.commit()
            print("ddddddddddddddd")
            login_user(new_user, remember=True)
            print("eeeeeeeeeeeeeee")
            flash('Account created!', category='success')
            print("ffffffffffffffff")
            return redirect(url_for('auth.show'))

    return render_template("sign_up.html", user=current_user)
