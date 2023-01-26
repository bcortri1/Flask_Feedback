from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """Form to register new users"""
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=8)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form to authenticate users"""
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=8)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])


class FeedbackForm(FlaskForm):
    """Form for users to provide feedback"""
    title = StringField("Title", validators=[InputRequired(), Length(min=8)])
    content = TextAreaField("Content", validators=[
                            InputRequired(), Length(min=8)])


class DeleteUserForm(FlaskForm):
    """Form to delete users, made for redundant CSRF protection"""
