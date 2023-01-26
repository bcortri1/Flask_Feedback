from flask import Flask, redirect, render_template, flash
from flask import session as s
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteUserForm
import subprocess


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "Super Secret"
debug = DebugToolbarExtension(app)

try:
    command = "psql -c 'create database feedback'"
    subprocess.call(command, shell=True)
except:
    print(Exception)


connect_db(app)

with app.app_context():
    db.create_all()


# ===================================GET=======================================
@app.route("/", methods=["GET"])
def redirect_register():
    """Redirect to register"""
    return redirect("/register")


@app.route("/register", methods=["GET"])
def register_form():
    """Renders registration form"""

    if "username" in s:
        return redirect(f"/users/{s['username']}")
    else:
        form = RegisterForm()
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET"])
def login_form():
    """Renders login form"""

    if "username" in s:
        return redirect(f"/users/{s['username']}")
    else:
        form = LoginForm()
        return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    """Clears session data and redirects to /"""
    s.pop("username")
    return redirect("/")


@app.route("/users/<string:username>", methods=["GET"])
def user_detail(username):
    """Renders details of current user, can delete user from this page"""
    form = DeleteUserForm()

    if "username" not in s or username != s['username']:
        flash("You must logged into that account!")
        return redirect("/")
    else:
        user = User.query.get_or_404(s['username'])
        return render_template("user_detail.html", user=user, form=form)


@app.route("/users/<string:username>/feedback/add", methods=["GET"])
def feedback_form_add(username):
    """Renders user feedback form"""

    form = FeedbackForm()
    user = User.query.get_or_404(username)

    if "username" not in s or username != s['username']:
        flash("Unauthorized!")
        return redirect("/")
    else:
        return render_template("feedback_create.html", user=user, form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET"])
def feedback_form_update(feedback_id):
    """Renders feedback update form"""

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    user = User.query.get_or_404(feedback.username)

    if "username" not in s or user.username != s['username']:
        flash("Unauthorized!")
        return redirect("/")
    else:
        return render_template("feedback_update.html", user=user, form=form)

# ===================================POST=======================================
@app.route("/register", methods=["POST"])
def create_user():
    """Handles registration of a new user"""
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.register(username, password)
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        s["username"] = username

        return redirect(f"/users/{username}")

    else:
        flash("Something Went Wrong")
        return render_template("register.html", form=form)


@app.route("/login", methods=["POST"])
def login_user():
    """Handles user authentication"""

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.authenticate(username, password):
            s["username"] = username
            return redirect(f"/users/{username}")

        else:
            flash("Invalid Combination")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/users/<string:username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes a user"""
    form = DeleteUserForm()
    user = User.query.get_or_404(s['username'])
    if form.validate_on_submit():
        if "username" in s and username == s['username']:
            s.pop("username")
            db.session.delete(user)
            db.session.commit()
            flash("Account Deleted!")
            return redirect("/")
        else:
            return render_template(f"/users/{s['username']}", form=form, user=user)
    return render_template(f"/users/{s['username']}", form=form, user=user)


@app.route("/users/<string:username>/feedback/add", methods=["POST"])
def create_feedback(username):
    """Handles feedback submission"""
    form = FeedbackForm()
    user = User.query.get_or_404(s['username'])
    if form.validate_on_submit():
        if "username" in s and username == s['username']:
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content,
                                username=user.username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{s['username']}")
        else:
            return redirect(f"/users/{s['username']}")
    return redirect(f"/users/{s['username']}")


@app.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    """Handles updating feedback submissions"""
    form = FeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get_or_404(feedback.username)
    if form.validate_on_submit():
        if "username" in s and user.username == s['username']:
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f"/users/{s['username']}")
        else:
            return redirect(f"/users/{s['username']}")
    return redirect(f"/users/{s['username']}")


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Handles feedback deletion"""

    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get_or_404(feedback.username)

    if "username" in s and user.username == s['username']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{s['username']}")
    else:
        return redirect(f"/users/{s['username']}")
