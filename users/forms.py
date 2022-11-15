import re

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo



def character_check(form, field):

    excluded = "*?!'^+%&/()=}][{$#@<>"

    for char in field.data:
        if char in excluded:
            raise ValidationError(f'Character {char} is not allowed')


class RegisterForm(FlaskForm):

    def validate_phone(self, data_field):
        reg = re.compile("\d{4}-\d{3}-\d{4}")

        if not reg.match(data_field.data):
            raise ValidationError("Phone number must be in format: XXXX-XXX-XXXX")

    def look_ahead(self, data_field):
        reg = re.compile("(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)")
        print(data_field.data)
        if not reg.match(data_field.data):
            raise ValidationError("Must contain: 1 digit, 1 lower-case, 1 upper-case, 1 non-letter character")

    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[character_check, DataRequired()])
    lastname = StringField(validators=[DataRequired(), character_check])
    phone = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), look_ahead])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both passwords must be '
                                                                                             'equal')])
    submit = SubmitField(validators=[DataRequired()])


class LoginForm(FlaskForm):

    username = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])

    pin = StringField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()
