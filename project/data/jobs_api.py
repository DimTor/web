import flask
from flask import request
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished', 'team_leader'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'job', 'work_size', 'collaborators', 'start_date',
                                       'end_date', 'is_finished', 'team_leader'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    db_sess = db_session.create_session()
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader']):
        return flask.jsonify({'error': 'Bad request'})
    elif db_sess.query(Jobs).filter(Jobs.id==request.json['id']).first():
        return flask.jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['POST'])
def edit_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    jobs.id=jobs_id
    jobs.job=request.json['job']
    jobs.work_size=request.json['work_size']
    jobs.collaborators=request.json['collaborators']
    jobs.start_date=request.json['start_date']
    jobs.end_date=request.json['end_date']
    jobs.is_finished=request.json['is_finished']
    jobs.team_leader=request.json['team_leader']
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})