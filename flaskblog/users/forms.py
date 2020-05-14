
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=2, max=20, message='username')]
    )
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up')

    # costum validation, prevent database fall ( same name / email )
    def validate_username(self, username):
        # look for user in database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Name already in use')

    def validate_email(self, email):
        # look for email in database
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('email in use')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('login')


class UpdateAccountForm(FlaskForm):
    username = StringField('username', validators=[
                           DataRequired(), Length(min=2, max=20, message='username')])
    picture = FileField('Update profile picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('update')

    # costum validation, prevent database fall ( same name / email )
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Name already in use')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('email in use')


class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError(
                'No Email in db, please check your spelling right !')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')