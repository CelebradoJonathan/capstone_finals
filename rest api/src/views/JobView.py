from flask import request, json, Response, Blueprint

from ..models.JobModel import JobModel, JobSchema


job_api = Blueprint('jobs', __name__)

job_schema = JobSchema()


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


@job_api.route('/', methods=['POST'])
def create():
    """
    Create Job Function
    """

    req_data = request.get_json()
    print(str(req_data))
    data, error = job_schema.load(req_data)
    if error:
        return custom_response(error, 404)
    job = JobModel(data)
    job.save()
    job_message = job_schema.dump(job)

    return custom_response(job_message, 201)


@job_api.route('/<string:job_id>', methods=['GET'])
def get_a_job(job_id):
    """
    Get jobs according to job_id
    """

    job = JobModel.get_one_job(job_id)
    if not job:
        return custom_response({'error': 'job not found'}, 404)

    job_message = job_schema.dump(job, many=True)
    return custom_response(job_message, 200)


@job_api.route('', methods=['GET'])
def get_all_job():
    """
    Get a all jobs
    """
    job = JobModel.get_all_jobs()

    if not job:
        return custom_response({'error': 'no job found'}, 404)
    job_message = job_schema.dump(job, many=True)
    return custom_response(job_message, 200)


@job_api.route('/<int:id>/<string:job_id>', methods=['PUT'])
def update(id, job_id):
    """
    Update a job based on id anf job_id
    """
    req_data = request.get_json()
    job = JobModel.get_one_job_only(id, job_id)
    if not job:
        return custom_response({'error': 'job not found'}, 404)

    data, error = job_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    job.update(data)

    job_message = job_schema.dump(job)
    return custom_response(job_message, 200)


@job_api.route('/<string:job_id>', methods=['PUT'])
def update_all(job_id):
    """
    Update a job based on id anf job_id
    """
    req_data = request.get_json()
    job = JobModel.get_one_job(job_id)
    if not job:
        return custom_response({'error': 'job not found'}, 404)

    data, error = job_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    for ajob in job:
        ajob.update(data)
        job_message = job_schema.dump(ajob)

    return custom_response(job_message, 200)


@job_api.route('/<string:job_id>', methods=['DELETE'])
def delete(job_id):
    """
    Delete all jobs based on the given job_id
    """

    job = JobModel.get_one_job(job_id)

    if not job:
        return custom_response({'error': 'job not found'}, 404)

    JobModel.query.filter(JobModel.job_id == job_id).delete()

    return custom_response({'message': 'deleted'}, 204)



