import pytest
from app.jobs.models import JobOffer
from app.jobs.services import (create_job, list_job, get_job, update_job, delete_job)



class TestJobsService:

    def test_create_job_success(self):
        data = {
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "image": "https://example.com/logo.png",
            "location": "Málaga",
            "movility": "Presencial",
            "salary": 15000,
            "description": "Test",
            "url": "https://example.com/job/1",
            "skills": ["Python", "Django", "React"],
            "experience_required": "2 years",
            "seniority": "mid",
            "type_contract": "indefinido"
        }

        job = create_job(data)
        assert job.title == "Full Stack Developer"
        assert job.company == "Tech Company"
        assert job.image == "https://example.com/logo.png"
        assert job.location == "Málaga"
        assert job.movility == "Presencial"
        assert job.salary == 15000
        assert job.description == "Test"
        assert job.url == "https://example.com/job/1"
        assert job.skills == ["Python", "Django", "React"]
        assert job.experience_required == "2 years"
        assert job.seniority == "mid"
        assert job.type_contract == "indefinido"

        assert JobOffer.objects.count() == 1

    def test_list_jobs_without_filter(self):
        create_job({
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "location": "Málaga",
            "url": "https://example.com/job/1",
        })
        create_job({
            "title": "Backend Developer",
            "company": "Another Company",
            "location": "Madrid",
            "url": "https://example.com/job/2",
        })

        jobs = list_job()
        assert len(jobs) == 2

    def test_list_jobs_with_filter(self):
        create_job({
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "location": "Málaga",
                "url": "https://example.com/job/1",
        })
        create_job({
            "title": "Backend Developer",
            "company": "Another Company",
            "location": "Madrid",
            "url": "https://example.com/job/2",
        })


        filters = {"location": "Mála"}
        jobs = list_job(filters=filters)
        assert len(jobs) == 1

    def test_get_job_succes(self):
        job = create_job({
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "location": "Málaga",
            "url": "https://example.com/job/1",
        })
        
        found_job = get_job(job.id)
        assert found_job is not None
        assert found_job.title == "Full Stack Developer"

    def test_get_job_not_found(self):
        found_job = get_job("nonexistent_id")
        assert found_job is None

    def test_update_job_success(self):
        job = create_job({
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "location": "Málaga",
            "url": "https://example.com/job/1",
        })

        update_data = {"title": "Senior Full Stack Developer"}
        updated_job = update_job(job.id, update_data)

        assert updated_job is not None
        assert updated_job.title == "Senior Full Stack Developer"

    def test_update_job_not_found(self):
        response = update_job("nonexistent_id", {"title": "New"})
        
        assert response == 'La oferta con ese id no ha sido encontardo.'

    def test_delete_job_success(self):
        job = create_job({
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "location": "Málaga",
            "url": "https://example.com/job/1",
        })

        assert JobOffer.objects.count() == 1

        response = delete_job(job.id)

        assert response == {'name': 'Full Stack Developer', 'company': 'Tech Company'}
        assert JobOffer.objects.count() == 0

    def test_delete_job_not_found(self):
        response = delete_job("nonexistent_id")
        assert response is None