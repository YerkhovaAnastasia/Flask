from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def ff():
    return render_template('base.html', title='Заготовка')


if __name__ == '__main__':
    print(app.run(debug=True))