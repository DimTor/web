import json
import random

from flask import Flask, render_template, request, url_for, redirect
from data.loginform import LoginForm
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
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


@app.route('/list_prof/<list>')
def draw_list(list):
    return render_template('ex2.html', list=list)


@app.route('/promotion')
def promotion():
    m = ['Человечество вырастает из детства.', 'Человечеству мала одна планета.',
         'Мы сделаем обитаемыми безжизненные пока планеты.', 'И начнем с Марса!', 'Присоединяйся!']
    return '</br>'.join(m)


@app.route('/image_mars')
def image():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <title>Привет, Яндекс!</title>
                      </head>
                      <body>
                        <h1>Привет, Марс</h1>
                        <img src="{url_for('static', filename='img/riana.jpg')}" width="100" height="100">
                        <p>Вот она какая</p>
                      </body>
                    </html>"""


@app.route('/promotion_image')
def bootstrap():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/st1.css')}" />
                    <title>Привет, Яндекс!</title>
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                  </head>
                  <body>
                    <h1>Привет, Яндекс!</h1>
                    <img src="{url_for('static', filename='img/riana.jpg')}" width="100" height="100">
                       <div class="alert alert-primary" role="alert">
                      Марс
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      Жди
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Придем
                    </div>
                    <div class="alert alert-success" role="alert">
                      Скоро....
                    </div>
                  </body>
                </html>'''


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        answer['surname'] = request.form.get('surname')
        answer['name'] = request.form.get('name')
        answer['education'] = request.form.get('class')
        answer['profession'] = ', '.join(request.form.getlist('accept'))
        answer['sex'] = request.form.get('sex')
        if request.form.get('accept7'):
            answer['motivation'] = request.form.get('accept7')
        else:
            answer['motivation'] = 'нет'
        answer['ready'] = request.form.get('se')

        return "Форма отправлена"


@app.route('/choice/<planet_name>')
def planeta(planet_name):
    return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/st1.css')}" />
                        <title>Привет, {planet_name}</title>
                        <link rel="stylesheet" 
                        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                        crossorigin="anonymous">
                      </head>
                      <body>
                        <h1>Привет, {planet_name}!</h1>
                           <div class="alert alert-primary" role="alert">
                          {planet_name}
                        </div>
                        <div class="alert alert-secondary" role="alert">
                          Жди
                        </div>
                        <div class="alert alert-danger" role="alert">
                          Придем
                        </div>
                        <div class="alert alert-success" role="alert">
                          Скоро....
                        </div>
                      </body>
                    </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def result(nickname, level, rating):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/st1.css')}" />
                    <title>Привет, Яндекс!</title>
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                  </head>
                  <body>
                    <h1>Здравствуйте, {nickname}!</h1>
                       <div class="alert alert-primary" role="alert">
                      Ваш рейтинг после {str(level)} этапа отбора
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      Составляет {str(rating)}
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Круто!
                    </div>
                  </body>
                </html>'''


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    return render_template('auto_answer.html', surname=answer['surname'], name=answer['name'],
                           education=answer['education'], prof=answer['profession'], sex=answer['sex'],
                           mot=answer['motivation'], ready=answer['ready'])


answer = {}


@app.route('/distribution')
def distrib():
    name = ['Tom', 'Sam', 'Ridlly', 'York']
    return render_template('distribution.html', name=name)


@app.route('/table/<sex>/<int:years>')
def table(sex, years):
    typ = 1
    if sex == 'male' and years < 21:
        typ = 1
    elif sex == 'male' and years >= 21:
        typ = 2
    elif sex == 'female' and years < 21:
        typ = 3
    elif sex == 'female' and years >= 21:
        typ = 4
    return render_template('table.html', type=typ)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', form=form)


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    if request.method == 'GET':
        return render_template('load_photo.html', pic=True)
    elif request.method == 'POST':
        f = request.files['file']
        z = open(f'static/img/{f.filename}', 'wb')
        z.write(f.read())
        z.close()
        s = f'../../static/img/{f.filename}'
        return render_template('load_photo.html', pic=False, name=s)


@app.route('/carousel')
def carousel():
    return render_template('carousel.html')


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    if request.method == 'GET':
        directory = 'static/img'
        files = os.listdir(directory)
        file = []
        for n, i in enumerate(files):
            if n == 0:
                continue
            file.append(f'../../static/img/{i}')
        return render_template('galery.html', img=file)
    elif request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        z = open(f'static/img/{f.filename}', 'wb')
        z.write(f.read())
        z.close()
        directory = 'static/img'
        files = os.listdir(directory)
        file = []
        for n, i in enumerate(files):
            if i == 'alien_1.png':
                continue
            file.append(f'../../static/img/{i}')
        return render_template('galery.html', img=file)


@app.route('/member')
def member():
    number = random.randint(0, 4)
    with open('templates/json.json', 'r') as fj:
        file = json.load(fj)[number]
        name = file['surname'] + ' ' + file['name']
        photo = file['photo']
        speciality = file['speciality']
    return render_template('member.html', name=name, photo=photo, speciality=speciality)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
