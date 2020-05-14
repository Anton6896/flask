
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,  # author = current_user
        )
        db.session.add(post)
        db.session.commit()

        flash('Your post is created !', 'success')
        return redirect(url_for('main.home'))

    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)

    return render_template('new_post.html', title='new post',
                           image_file=image_file, form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if post.user_id != current_user.id:
        abort(403)  # return the error

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # no need to create new one
        flash('Post updated !', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    """
    will use here same new post html file but update the variables in it
    """
    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)

    return render_template('new_post.html', title='Update post',
                           image_file=image_file, form=form, legend='Update post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # find post
    post_title = post.title
    if post.author != current_user:  # user access
        abort(403)
    db.session.delete(post)  # delete post
    db.session.commit()
    flash(f'Post : {post_title}, deleted !', 'success')

    return redirect(url_for('main.home'))