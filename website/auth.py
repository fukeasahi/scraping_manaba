from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
  return render_template("login.html", boolean = False)

@auth.route("/logout")
def logout():
  return "logout"

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
  if request.method == "POST":
    email           = request.form.get("email")
    firstName       = request.form.get("firstName")
    password1       = request.form.get("password1")
    password2       = request.form.get("password2")
    manabaUserName  = request.form.get("manabaUserName")
    manabaPassword1 = request.form.get("manabaPassword1")
    manabaPassword2 = request.form.get("manabaPassword2")
    lineApiToken1   = request.form.get("lineApiToken1")
    lineApiToken2   = request.form.get("lineApiToken2")

    if len(email) < 4:
      flash("Email must be greater than 4 characyers.", category="error")
    elif len(firstName) < 2:
      flash("First name must be greater than 2 characyers.", category="error")
    elif password1 != password2:
      flash("Passwords don\'t match.", category="error")
    elif len(password1) < 7:
      flash("Passwords must be greater than 7 characyers.", category="error")
    elif len(manabaUserName) < 7:
      flash("manaba User Name must be greater than 7 characyers.", category="error")
    elif manabaPassword1 != manabaPassword2:
      flash("manabaPassword don\'t match.", category="error")
    elif len(manabaPassword1) < 7:
      flash("manaba Password must be greater than 7 characyers.", category="error")
    elif lineApiToken1 != lineApiToken2:
      flash("lineApiToken don\'t match.", category="error")
    elif len(lineApiToken1) < 7:
      flash("ineApiToken must be greater than 7 characyers.", category="error")
    else:
      # add user Database
      flash("Account created!", category="success")

  return render_template("sign_up.html")
