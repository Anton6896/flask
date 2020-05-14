from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from .forms import (RegistrationForm, LoginForm,
                    UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from .utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password , and add all data to the db
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')  # decode to String
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)  # create db entries
        db.session.commit()  # update db entries
        login_user(user, remember=False)  # log user to site
        # success ->  bootstap class
        flash('account is created , wellcome', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()  # query db for user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # remember=True/False
            login_user(user, remember=form.remember.data)
            """
            if user asked to get some page but have no access ,
            after authentication will be redirected to this page
            """
            next_page = request.args.get('next')  # if args exist -> next_page
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('bad email or password', 'danger')
    return render_template('login.html', title='login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()  # get user
    page = request.args.get('page', 1, type=int)
    query = Post.query\
        .filter_by(user_id=user.id)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('user_post.html', posts=query, user=user, title='home')


# restricted route , only logged users can see
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)
    posts = Post.query.filter_by(user_id=current_user.id)

    return render_template('account.html', title='account', image_file=image_file, form=form, posts=posts)


""" 
handle the password reset by the mail to user , 
updated User model by adding get_reset_token, verify_reset_token. 
with using itsdangerous lib. that allow generate token for periud of time .
pip install flask-mail
"""
@users.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    # sending the mail with reset token
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():  # get user that ask for password change
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)  # send password reset link with timed token
        flash('email was send with instractions ', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='reset request', form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    # cheking the users toke and
    # reseting password in db
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)  # return user instance
    if user is None:
        flash('time limit rich with token.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        login_user(user, remember=False)
        flash('password was updated', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='reset token', form=form)
