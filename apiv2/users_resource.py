from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort

from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position')


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"user {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'age'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'surname', 'name', 'age')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'], 
            surname=args['id'], 
            name=args['name'],
            age=args['age'], 
            position=args['position']
        )
        try:
            session.add(user)
        except Exception as e:
            return jsonify({'error': e})
        session.commit()
        return jsonify({'success': 'OK'})
