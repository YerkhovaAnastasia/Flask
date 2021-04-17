from flask import Flask, render_template, redirect
from flask_login import login_user
from forms.login import LoginForm
from db.user import User
from forms.register import RegisterForm
from db import db_session

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def ff():
    return render_template('base.html', title='Заготовка')

@app.route('/registratsia', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            # au_attitude=form.au_attitude.data,
            # frog_attitude=form.frog_attitude.data,
            # cvc_code=form.cvc_code.data,
            # modified_date=dt.date.today()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/vhod', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


if __name__ == '__main__':
    print(app.run(debug=True))