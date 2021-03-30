from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from requests import post
from data import db_session, jobs_api
from data.add_job import AddJobForm
from data.login_form import LoginForm
from data.users import User
from data.jobs import Jobs
from data.register import RegisterForm
from flask_restful import reqparse, abort, Api, Resource
from data.users_resource import UsersListResource
from data.users_resource import UsersResource
from data.jobs_resource import JobsResource
from data.jobs_resource import JobsListResource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
# для списка объектов
api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(JobsListResource, '/api/v2/jobs')

# для одного объекта
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(JobsResource, '/api/v2/jobs/<int:jobs_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()

    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(
            job=add_form.job.data,
            team_leader=add_form.team_leader.data,
            work_size=add_form.work_size.data,
            collaborators=add_form.collaborators.data,
            is_finished=add_form.is_finished.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a job', form=add_form)


@app.route('/editjob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def editjob(job_id):
    add_form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                              ).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                              Jobs.user == current_user
                                              ).first()
        if jobs:
            add_form.job.data = jobs.job
            add_form.team_leader.data = jobs.team_leader
            add_form.work_size.data = jobs.work_size
            add_form.collaborators.data = jobs.collaborators
            add_form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = add_form.job.data
            jobs.team_leader = add_form.team_leader.data
            jobs.work_size = add_form.work_size.data
            jobs.collaborators = add_form.collaborators.data
            jobs.is_finished = add_form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование новости',
                           form=add_form
                           )


@app.route('/jobs_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def news_delete(job_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                          ).first()
    else:
        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                          Jobs.user == current_user
                                          ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
