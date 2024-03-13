from flask import Blueprint, request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, current_user, login_required, logout_user
from Models import User, Post
from blog import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from blog.users.forms import RegisterForm, RequestResetForm, UpdateAccountForm, ResetPasswordForm, LoginForm
from blog.users.utils import *



users= Blueprint('users', __name__)


@users.route('/register', methods =['POST', 'GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard_page'))
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        gender = form.gender.data
        nationality = form.nationality.data

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user and add to the database
        user_to_create = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hashed_password,
            image_file=save_picture(form.image_file.data),
            gender=gender,
            nationality=nationality,
        )
        
        db.session.add(user_to_create)
        db.session.commit()

         # Generate a confirmation token and send the verification email
        # confirmation_token = user_to_create.generate_confirmation_token()
        # confirmation_url = url_for('users.confirm_email', token=confirmation_token, _external=True)
        # send_verification_email(user_to_create, confirmation_url)

        flash(f"Registration successful! A confirmation email has been sent to {user_to_create.email}.", category='success')
        return redirect(url_for('users.login_page'))
        
    elif form.errors:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='danger')

    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods = ['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard_page'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        attempted_user = User.query.filter_by(username=username).first()
        if attempted_user and check_password_hash(attempted_user.password_hash, password):
            login_user(attempted_user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login Successful!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('users.dashboard_page'))
        else:
            flash(f'Username and password do not match! Please try again', category='danger') 
    return render_template('login.html', form = form, title='Login')



@users.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out, hope to see you soon!", category='info')
    return redirect(url_for('users.login_page'))



@users.route('/notifications')
@login_required
def notification_page():
    return render_template('notification.html', title='Notification')




@users.route('/dashboard', methods =['POST', 'GET'])
@login_required
def dashboard_page():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('dashboard.html',title='Dashboard', image_file=image_file)



@users.route('/Update', methods =['POST', 'GET'])
@login_required
def update_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.image_file = save_picture(form.image_file.data)
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.bio=form.bio.data
        db.session.commit()
        # Refresh the current user object after committing changes
        db.session.refresh(current_user)
        flash('Your account has been updated!', category='success')
        return redirect(url_for('users.dashboard_page'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        form.bio.data=current_user.bio
        
    return render_template('update account.html', title='Update Account', form=form)



@users.route('/user/<string:username>')
@login_required
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    
    # Use has method for relationship comparison
    posts = Post.query.filter(Post.author.has(id=user.id))\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    
    return render_template('user_posts.html', posts=posts, title='Blogs', user=user)


@users.route('/confirm/<token>')
def confirm_email(token):
    user = User.query.filter_by(confirmation_token=token).first()

    if user:
        if user.confirmed:
            flash('Email already confirmed. Please log in.', category='info')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            flash('Email confirmed. You can now log in.', category='success')
    else:
        flash('Invalid or expired confirmation link. Please register again.', category='danger')

    return redirect(url_for('users.login_page'))

@users.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email('auth/email/confirm','Confirm Your Account', user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@users.route('/reset_password', methods =['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard_page'))
    form = RequestResetForm()
    if form.validate_on_submit:
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', category='info')
            return redirect(url_for('users.login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods =['POST', 'GET'])
def reset_token(token):
        if current_user.is_authenticated:
            return redirect(url_for('users.dashboard_page'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', category='warning')
            return redirect(url_for('users.reset_password'))
        form = ResetPasswordForm()
        if (form.validate_on_submit()):
            password = form.password.data
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            user.password=hashed_password
            db.session.commit()
            flash("Password reset successful! You are now able log in.", category='success')
            return redirect(url_for('users.login_page'))
        return render_template('reset_token.html', title='Reset Password', form = form)

