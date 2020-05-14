from flask import render_template, request, Blueprint, url_for
from flaskblog.models import Post
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # query = Post.query.all()
    # query = Post.query.order_by(Post.date_posted.desc()).all()

    # pagination
    page = request.args.get('page', 1, type=int)
    query = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=query, title='home')


@main.route('/about')
def about():
    us = current_user
    user_pic = url_for(
        'static', filename='profile_pics/'+current_user.image_file)

    return render_template('about.html', us=us, image=user_pic)