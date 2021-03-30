from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.works import Jobs

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message="Job not found")


def check_unique_constant(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if jobs:
        abort(404, message="Job with this id already exists")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job',
                  'work_size', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'job': [item.to_dict(
            only=('team_leader', 'job', 'id',
                  'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished')) for item in job]})

    def post(self):
        args = parser.parse_args()
        check_unique_constant(args['id'])
        session = db_session.create_session()
        job = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        try:
            session.add(job)
        except Exception as e:
            return jsonify({'error': e})
        session.commit()
        return jsonify({'success': 'OK'})
