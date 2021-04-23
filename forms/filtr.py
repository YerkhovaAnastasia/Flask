from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class Add_book(FlaskForm):
    autor = StringField('Автор', validators=[DataRequired()])
    name = StringField('Название книги', validators=[DataRequired()])
    gener = StringField('Жанр', validators=[DataRequired()])
    age = IntegerField('Год издания', validators=[DataRequired()])
    kr_soder = TextAreaField("Почему вы считаете себя не роботом?")
    my_reit = IntegerField('Мой рейтинг', validators=[DataRequired()])
    submit = SubmitField('Добавить книгу')
