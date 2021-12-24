from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, RadioField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class SignUpForm(FlaskForm):
    name = StringField("Имя: ", validators=[InputRequired(message="Это поле обязательно."),
                                            Length(min=4, max=10, message="Количество символов должно быть"
                                                                          " от 4 до 10.")])
    password = PasswordField("Пароль: ", validators=[InputRequired("Это поле обязательно"),
                                                     Length(min=6, max=15, message="Количество символов должно быть"
                                                                                   " от 6 до 15.")])
    password_confirm = PasswordField("Повторите пароль: ", validators=[EqualTo('password',
                                                                               message='Пароли не совпадают.')])
    email = EmailField("Email:", validators=[Email("Адрес электронной почты неверный.")])
    submit = SubmitField("Принять")


class RadioForm(FlaskForm):
    choice = RadioField(validators=[InputRequired("Выберете ответ.")])
    submit = SubmitField("Подтвердить выбор")


class StringForm(FlaskForm):
    answer = StringField(validators=[InputRequired("Введите ответ.")])
    submit = SubmitField("Подтвердить выбор")
