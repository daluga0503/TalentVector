from .models import JobOffer

def create_job(data):
    job = JobOffer(**data)
    job.save()
    return job

def list_job(filters=None):
    query = JobOffer.objects

    if filters:
        if 'location' in filters:
            query = query.filter(location=filters['location'])
        if 'seniority' in filters:
            query = query.filter(seniority=filters['seniority'])
        if 'skill' in filters:
            query = query.filter(skilss=filters['skill'])
    
    return query.order_by("-created_at")

def get_job(job_id):
    return JobOffer.objects(id=job_id).first()

def upadte_job(job_id, data):
    job = get_job(job_id)

    if not job:
        return 'La oferta con ese id no ha sido encontardo.'
    
    for key, value in data.items():
        setattr(key, value)

    job.save()
    return job

def delete_job(job_id):
    job = get_job(job_id)
    if not job:
        return None
    job_info = {'name':job.title, 'company':job.company}
    job.delete()
    return job_info
