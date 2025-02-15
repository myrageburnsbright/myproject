from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,PasswordField,SubmitField,FileField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,EqualTo, ValidationError
from .models.user import User
from flask import current_app
import os

class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=2,max=100)])
    login = StringField('Логин', validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Пароль',validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',validators=[DataRequired(), EqualTo('password')])
    avatar = FileField("Загрузите аватар",validators=[DataRequired(), FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField("Зарегестрирроваться")

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError("Данное имя пользователя уже занято. Пожалуйста, выберите другое...")
        
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Пароль',validators=[DataRequired()])
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")

class PostForm(FlaskForm):
    subject = StringField('Тема',validators=[DataRequired(), Length(min=1,max=50)])
    submit = SubmitField("Добавить")

class StudentForm(FlaskForm):
    student = SelectField('student', choices=[], render_kw={'class':'form-control'})

class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[], render_kw={'class':'form-control'})