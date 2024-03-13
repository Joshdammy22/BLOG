from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, EmailField, validators, TextAreaField, DateField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Email, DataRequired, ValidationError
from Models import User
from flask_login import current_user
import pycountry


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username') 

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email') 

    GENDER_CHOICES = [('Select your gender', 'Select your gender'),('Male', 'Male'), ('Female', 'Female'), ('other', 'Other')]

    # Get a list of all countries sorted by name
    COUNTRY_CHOICES =[(country.name, country.name) for country in pycountry.countries]

    full_name = StringField(label='First and Last name', validators=[Length(max=120, message='Full name should not exceed 120 characters.'), DataRequired(message='Full name is required.')])
    username = StringField(label='Username', validators=[Length(min=5, max=20, message='Username must be between 5 and 20 characters.'), DataRequired(message='Username is required.')])
    password = PasswordField(label='Password:', validators=[Length(min=8, max=20, message='Password must be between 8 and 20 characters.'), DataRequired(message='Password is required.')])
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired(message='Passwords must match.')])
    bio = TextAreaField(label='Tell us something amazing about yourself')
    image_file = FileField(label='Choose Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email = EmailField(label='Email Address', validators=[Email(), DataRequired(message='Email is required.')])
    gender = SelectField(label='Gender', choices=GENDER_CHOICES, validators=[DataRequired(message='Select your gender')])
    nationality = SelectField(label='Nationality', choices=COUNTRY_CHOICES, validators=[DataRequired()])
    date_of_birth = DateField(label='Date of Birth')  # You can replace this with a DateField if you want to capture a date
    submit = SubmitField(label='Sign Up')
    

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField(label='Sign in')


class UpdateAccountForm(FlaskForm):
    def validate_username(self, username_to_check):
        if username_to_check.data != current_user.username:
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists! Please try a different username') 

    def validate_email(self, email_to_check):
        if email_to_check.data != current_user.email:
            email = User.query.filter_by(email=email_to_check.data).first()
            if email:
                raise ValidationError('Email already exists! Please try a different email') 
    
    username = StringField(label='Username', validators=[Length(min=5, max=20, message='Username must be between 5 and 20 characters.'), DataRequired(message='Username is required.')])
    bio = TextAreaField(label='Tell us something amazing about yourself')
    image_file = FileField(label='Choose Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email = EmailField(label='Email Address', validators=[Email(), DataRequired(message='Email is required.')])
    submit = SubmitField(label='Save Changes')
    



class RequestResetForm(FlaskForm):
    email = EmailField(label='Email Address', validators=[Email(), DataRequired(message='Email is required.')])
    submit = SubmitField(label='Request Password Reset')
    def validate_email(self, email_to_check):
        if email_to_check.data != current_user.email:
            email = User.query.filter_by(email=email_to_check.data).first()
            if email:
                raise ValidationError('There is no account with that email, you must register first!') 



class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password:', validators=[Length(min=8, max=20, message='Password must be between 8 and 20 characters.'), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Reset Password')