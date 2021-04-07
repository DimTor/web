import flask
from flask import request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                    'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'users': users.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                         'speciality', 'address', 'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    db_sess = db_session.create_session()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email']):
        return flask.jsonify({'error': 'Bad request'})
    elif db_sess.query(User).filter(User.id == request.json['id']).first():
        return flask.jsonify({'error': 'Id already exists'})
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(users)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['POST'])
def edit_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return flask.jsonify({'error': 'Not found'})
    users = db_sess.query(User).filter(User.id == users_id).first()
    users.id=users_id
    users.surname=request.json['surname']
    users.name=request.json['name']
    users.age=request.json['age']
    users.position=request.json['position']
    users.speciality=request.json['speciality']
    users.address=request.json['address']
    users.email=request.json['email']
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users_show/<int:user_id>', methods=['GET'])
def city_from(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    return flask.jsonify({'users': users.to_dict(only=('surname', 'name', 'city_from'))})
