from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])


class ChangeNumber(FlaskForm):
    contact_number = StringField('Номер телефона', validators=[DataRequired()])


class ChangeAddress(FlaskForm):
    address = StringField('Адрес', validators=[DataRequired()])


class ChangeCount(FlaskForm):
    count = IntegerField('Количество', validators=[DataRequired()])