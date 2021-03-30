from flask import Flask, render_template, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from requests import get
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from apiv2 import users_resource, jobs_resource
from api import jobs_api, user_api
from Froms import RegisterJobForm, LoginForm, RegisterForm, RegisterDepartmentForm
from data import db_session
from data.db_session import create_session
from data.department import Department
from data.users import User
from data.works import Jobs

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = RegisterJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job_title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавление работы', form=form)


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
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = RegisterJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id
                                         ).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job_title.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id
                                         ).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job_title.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Department).filter(Department.id == id,
                                            ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/department")
def department_log():
    db_sess = create_session()
    return render_template("department_log.html", departments=db_sess.query(Department).all())


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = RegisterDepartmentForm()
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id
                                                  ).first()
    if department:
        if request.method == "GET":
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        if form.validate_on_submit():
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data

            db_sess.commit()
            return redirect('/department')
    else:
        abort(404)
    return render_template('add_department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/add_department', methods=['GET', 'POST'])
def add_dep():
    form = RegisterDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/')
    return render_template('add_department.html', title='Добавление департамента', form=form)


@app.route("/")
def work_log():
    db_sess = create_session()
    return render_template("work_log.html", jobs=db_sess.query(Jobs).all())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def get_ll_spn(toponym):
    toponym_upper_lower = toponym["boundedBy"]["Envelope"]
    toponym_upper, toponym_lower = toponym_upper_lower["lowerCorner"].split(" ")
    toponym_upper_2, toponym_lower_2 = toponym_upper_lower["upperCorner"].split(" ")

    delta_1 = round(abs(float(toponym_lower) - float(toponym_lower_2)) / 2, 6)
    delta_2 = round(abs(float(toponym_upper) - float(toponym_upper_2)) / 2, 6)
    return toponym["Point"]["pos"].replace(" ", ","), f"{delta_1},{delta_2}"


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    user = get(f'http://localhost:5000/api/user/{user_id}').json()['users']
    if 'error' in user:
        return "User not found"
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": user['city_from']
    })

    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn(toponym)

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    return render_template("users_show.html", image=static_api_request, user=user)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)

    api.add_resource(users_resource.UserListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/user/<int:user_id>')
    api.add_resource(jobs_resource.JobListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/job/<int:job_id>')

    app.run()


if __name__ == '__main__':
    main()
