from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<title>')
@app.route('/index/<title>')
def index(title='Noname'):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def spec(prof):
    if 'инженер' in prof or 'строитель' in prof:
        pr = "/static/img/mars.jpg"
    else:
        pr = "/static/img/MARS-2-2.png"
        print('fff')
    return render_template('ex1.html', prof=pr)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
