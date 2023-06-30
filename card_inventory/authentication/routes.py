from flask import Blueprint, render_template, request, redirect, url_for, flash
from card_inventory.forms import UserLoginForm
from card_inventory.models import User, db, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    userform = UserLoginForm()

    try:
        if request.method == "POST" and userform.validate_on_submit():
            username = userform.username.data
            email = userform.email.data
            password = userform.password.data
            print(email, password)

            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account, {username}.", "user-created")
            return redirect(url_for("auth.signin"))
    except:
        raise Exception("Invalid sign up data. Please try again.")
    return render_template("signup.html", form=userform)

@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    userform = UserLoginForm()
    try:
        if request.method == "POST" and userform.validate_on_submit():
            username = userform.username.data
            email = userform.email.data
            password = userform.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash(f"{username} has logged in.")
                return redirect(url_for("site.profile")) 
            else:
                flash("Your email or password is incorrect", "auth-failed")
                return redirect("auth.signin")
    except:
        raise Exception("Invalid sign in data, please try again.")
    return render_template("signin.html", form=userform)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.home"))