from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, \
    DateTimeField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterJobForm(FlaskForm):
    job_title = StringField('job_title', validators=[DataRequired()])
    team_leader = StringField('team_leader', validators=[DataRequired()])
    work_size = IntegerField("work_size", validators=[DataRequired()])
    collaborators = StringField("collaborators", validators=[DataRequired()])
    start_date = DateTimeField("start_date")
    end_date = DateTimeField("end_date")
    is_finished = BooleanField("is_finished")
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта/ Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = TextAreaField("Возраст")
    position = TextAreaField("Позиция")
    speciality = TextAreaField("Специализация")
    submit = SubmitField('Зарегистрироваться')


class RegisterDepartmentForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    chief = StringField('chief', validators=[DataRequired()])
    members = StringField("members", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    submit = SubmitField('submit')
