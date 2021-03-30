import flask
from flask import jsonify, request
from requests import get

from data.works import Jobs
from main import db_session

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=["GET"])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job',
                                    'work_size', 'collaborators'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/job/<int:job_id>', methods=["GET"])
def get_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'team_leader', 'job', 'id',
                'work_size', 'collaborators',
                'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'id',
                  'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif any(request.json['id'] == item['id']
             for item in get('http://localhost:5000/api/jobs').json()['jobs']):
        return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def change_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not jobs:
        return jsonify({'error': 'Not found'})

    correct_keys = ['team_leader', 'job', 'id',
                    'work_size', 'collaborators', 'is_finished']
    for key in request.json.keys():
        if key in correct_keys:
            exec(f'jobs.{key} = request.json["{key}"]')
        else:
            return jsonify({'error': f'Key {key} is not exists'})

    db_sess.commit()
    return jsonify({'success': 'OK'})
