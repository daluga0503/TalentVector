from app.jobs.models import JobOffer
from collections import Counter

def top_skills(limit=10):
    all_skills = []
    jobs = JobOffer.objects.only('skills')

    for job in jobs:
        all_skills.extend(job.skills)

    counter = Counter(all_skills)
    return counter.most_common(n=limit)

    
def top_locations(limit=10):
    all_locations = []
    jobs = JobOffer.objects.only('location')

    for job in jobs:
        all_locations.extend(job.location)

    counter = Counter(all_locations)
    return counter.most_common(limit)

def top_companies(limit=10):
    all_companies = []
    jobs = JobOffer.objects.only('company')

    for job in jobs:
        all_companies.extend(job.company)
    
    counter = Counter(all_companies)
    return counter.most_common(limit)

def seniority_distribution(limit=10):
    all_seniority = []
    jobs = JobOffer.objects.only('seniority')

    for job in jobs:
        all_seniority.extend(job.seniority)
    
    counter = Counter(all_seniority)
    return counter.most_common(limit)