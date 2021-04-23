from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms.login import LoginForm
from data.user import User
from data.book import Book
from forms.register import RegisterForm
from forms.filtr import AddBook
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def ff():
    if current_user.is_authenticated:
        return redirect('/user_page')
    return render_template('index.html', title='RePe')


@app.route('/user_page')
def user_page():
    return render_template('user_page.html', title='RePe')


@app.route('/razr')
def razr():
    return render_template('razrabotka.html', title='RePe')


@app.route('/filtr/<genre>')
def filtr(genre):
    db_sess = db_session.create_session()
    books = db_sess.query(Book).filter(Book.gener == genre).all()
    return render_template('geners.html', title='RePe', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBook()
    if form.gener.data not in ['Поэзия', 'Классика', 'Детектив', 'Боевик', 'Комедия', 'Ужастик', 'Фентези']:
        return render_template('filtr.html',
                               form=form,
                               message="Убедительная просьба выбрать жанр из нижеперечисленных: Поэзия,Классика,Детектив,Боевик,Комедия,Ужастик,Фентези")
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if db_sess.query(Book).filter(Book.name == form.name.data).first():
            return render_template('filtr.html',
                                   form=form,
                                   message="Такая книга уже записана")
        book = Book(
            autor=form.autor.data,
            name=form.name.data,
            gener=form.gener.data,
            age=form.age.data,
            kr_sod=form.kr_sod.data,
            my_reit=form.my_reit.data

            # au_attitude=form.au_attitude.data,
            # frog_attitude=form.frog_attitude.data,
            # cvc_code=form.cvc_code.data,
            # modified_date=dt.date.today()
        )
        db_sess.add(book)
        db_sess.commit()
        return redirect('/')
    return render_template('filtr.html', form=form)


@app.route('/registratsia', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html',
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
    return render_template('registr.html', form=form)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/user.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()
