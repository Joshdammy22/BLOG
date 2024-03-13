import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from PIL import Image
from blog import mail


def save_picture_post(form_picture):
    if form_picture and form_picture.filename != '':
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/UPLOAD_FOLDER', picture_fn)

        output_size = (1000, 1000)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn

    # Default image in case no file is uploaded
    return none
    





