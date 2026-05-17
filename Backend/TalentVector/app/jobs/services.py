from .models import JobOffer
from mongoengine.errors import ValidationError

def create_job(data):
    job = JobOffer(**data)
    job.save()
    return job

def list_job(filters=None):
    query = JobOffer.objects

    if filters:
        if 'location' in filters:
            query = query.filter(location__icontains=filters['location'])
        if 'seniority' in filters:
            query = query.filter(seniority__icontains=filters['seniority'])
        if 'skills' in filters:
            query = query.filter(skills__icontains=filters['skills'])
        if 'company' in filters:
            query = query.filter(company__icontains=filters['company'])
    
    return query.order_by("-created_at")

def get_job(job_id):
    try:
        return JobOffer.objects(id=job_id).first()
    except ValidationError:
        return None

def update_job(job_id, data):
    job = get_job(job_id)

    if not job:
        return None
    
    for key, value in data.items():
        setattr(job, key, value)

    job.save()
    return job

def delete_job(job_id):
    job = get_job(job_id)
    if not job:
        return None
    job_info = {'name':job.title, 'company':job.company}
    job.delete()
    return job_info
