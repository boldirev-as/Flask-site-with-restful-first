import flask
from flask import jsonify, request
from requests import get

from data.users import User
from data import db_session

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=["GET"])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name',
                                    'age'))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=(
                'id', 'surname', 'name',
                'age', 'position', 'speciality', 'city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name',
                  'age', 'position', 'speciality']):
        return jsonify({'error': 'Bad request'})
    elif any(request.json['id'] == item['id']
             for item in get('http://localhost:5000/api/users').json()['users']):
        return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    users = User(
        id=request.json['id'], surname=request.json['id'], name=request.json['name'],
        age=request.json['age'], position=request.json['position'], speciality=request.json['speciality']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def change_users(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == users_id).first()
    if not users:
        return jsonify({'error': 'Not found'})

    correct_keys = ['id', 'surname', 'name',
                    'age', 'position', 'speciality']
    for key in request.json.keys():
        if key in correct_keys:
            exec(f'users.{key} = request.json["{key}"]')
        else:
            return jsonify({'error': f'Key {key} is not exists'})

    db_sess.commit()
    return jsonify({'success': 'OK'})
