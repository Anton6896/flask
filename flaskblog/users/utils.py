
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from sqlalchemy.sql.functions import current_user  #! or not ? 


def save_picture(user_picture):
    # get the file from the form and save him to the
    # static foldel then return file name
    random_hex = secrets.token_hex(8)  # 8 bites
    _, f_ext = os.path.splitext(user_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # delete previous picture
    delete_picture()

    # resize and save new picture
    output_size = (125, 125)
    i = Image.open(user_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def delete_picture():
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', current_user.image_file
    )
    try:
        os.remove(picture_path)
    except OSError as e:
        print(f'Error: \n{picture_path}\n{e.strerror}')



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreplay@demo.com',
                  recipients=[user.email])
    # send link with token 
    msg.body = f""" to reset the password got here
    {url_for('users.reset_token', token=token, _external=True)} , 
    is you dint asked then just ignore it """
    mail.send(msg)