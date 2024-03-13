import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from PIL import Image
from blog import mail


def save_picture(form_picture):
    if form_picture and form_picture.filename != '':
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn

    # Default image in case no file is uploaded
    return 'default.jpg'
    
def send_verification_email(user):
    # Generate the confirmation URL
    confirmation_url = url_for('users.confirm_email', token=user.confirmation_token, _external=True)

    # Create the email message
    subject = 'Confirm Your Email Address'
    
    body = f'''
    Hi {user.full_name},

    Welcome to ProBlogging Platform! We're excited to have you on board.

    To activate your account and start exploring YourApp, please click the following link to confirm your email address:

    {confirmation_url}

    If you did not sign up, please ignore this email.

    Thank you,
    Support Team
    '''

    msg = Message(subject=subject, recipients=[user.email], body=body)

    # Send the email
    try:
        mail.send(msg)
        flash('A verification email has been sent. Please check your email to complete the registration.', category='info')
    except Exception as e:
        # Handle the exception (e.g., log the error)
        flash('An error occurred while sending the verification email. Please try again later.', category='danger')


def send_reset_email(user):
    if user is not None:
        token=user.get_reset_token()
        msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
        msg.body= f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

    
If you did not make this request then simply ignore this email and no change will be made.
''' 
        mail.send_reset_email(msg)