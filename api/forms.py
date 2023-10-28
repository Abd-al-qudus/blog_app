from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from flask_wtf import FlaskForm
from wtforms.validators import (
    InputRequired,
    Length,
    EqualTo,
    Email,
    Regexp,
    DataRequired,
    URL
)
from flask_ckeditor import CKEditorField

class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 300)])
    password = PasswordField(validators=[InputRequired(), Length(8, 300)])
    submit = SubmitField('login')
    

class register_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 300)])
    full_name = StringField(
        validators=[
            InputRequired(),
            Length(1, 300)
        ]
    )
    password = PasswordField(validators=[InputRequired(), Length(8, 300)])
    confirm_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 300),
            EqualTo("password", message="Passwords must match !"),
        ]
    )
    submit = SubmitField('register')

class CommentForm(FlaskForm):
    comment = CKEditorField("Comments:", validators=[DataRequired()])
    submit = SubmitField('comment')

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")