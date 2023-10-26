from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError
)
from flask_wtf import FlaskForm
from wtforms.validators import (
    InputRequired,
    Length,
    EqualTo,
    Email,
    Regexp
)


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 300)])
    password = PasswordField(validators=[InputRequired(), Length(1, 300)])
    submit = SubmitField('login')
    

class register_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 300)])
    full_name = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    password = PasswordField(validators=[InputRequired(), Length(1, 300)])
    confirm_password = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )
    submit = SubmitField('register')