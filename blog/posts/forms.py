from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, validators, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Email, DataRequired, ValidationError
from flask_ckeditor.fields import CKEditorField




class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')





class PostForm(FlaskForm):
    title=StringField(label="Title", validators=[DataRequired()])
    image_file = FileField(label='Choose Post Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    content= CKEditorField(label="Content", validators=[DataRequired()])
    submit=SubmitField(label='Post')
