import pytest
from app.jobs.models import JobOffer
from mongoengine.errors import NotUniqueError

class TestJobModel:

    def test_create_job_success(self):
        job = JobOffer(
            title= "Full Stack Developer",
            company = "Tech Company",
            image = "https://example.com/logo.png",
            location = "Málaga",
            movility = "Presencial",
            salary = 15000,
            description = "Test",
            url = "https://example.com/job/1",
            skills = ["Python", "Django", "React"],
            experience_required = "2 years",
            seniority = "mid",
            type_contract = "indefinido"
        ).save()
        
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

    def test_url_job_is_unique(self):
        JobOffer(
            title= "Full Stack Developer",
            company = "Tech Company",
            image = "https://example.com/logo.png",
            location = "Málaga",
            movility = "Presencial",
            salary = 15000,
            description = "Test",
            url = "https://example.com/job/1",
            skills = ["Python", "Django", "React"],
            experience_required = "2 years",
            seniority = "mid",
            type_contract = "indefinido"
        ).save()
        with pytest.raises(NotUniqueError):
            JobOffer(
                title= "Full Stack Developer",
                company = "Tech Company",
                image = "https://example.com/logo.png",
                location = "Málaga",
                movility = "Presencial",
                salary = 15000,
                description = "Test",
                url = "https://example.com/job/1",
                skills = ["Python", "Django", "React"],
                experience_required = "2 years",
                seniority = "mid",
                type_contract = "indefinido"
        ).save()
    
    def test_job_creation_without_required_fields(self):
        with pytest.raises(Exception):
            JobOffer(
                company = "Tech Company",
                url = "https://example.com/job/1"
            ).save()
        with pytest.raises(Exception):
            JobOffer(
                title= "Full Stack Developer",
                url = "https://example.com/job/1"
            ).save()
        with pytest.raises(Exception):
            JobOffer(
                title= "Full Stack Developer",
                company = "Tech Company"
            ).save()

    def test_job_missing_optional_fields(self):
        job = JobOffer(
            title= "Full Stack Developer",
            company = "Tech Company",
            url = "https://example.com/job/1"
        ).save()
        assert job.title == "Full Stack Developer"
        assert job.company == "Tech Company"
        assert job.url == "https://example.com/job/1"
        assert job.image == None
        assert job.location == None
        assert job.movility == None
        assert job.salary == None
        assert job.description == None
        assert job.skills == []
        assert job.experience_required == None
        assert job.seniority == "junior"
        assert job.type_contract == None

    def test_seniority_choices(self):
        seniority_values = ['junior', 'mid', 'senior', 'architecture', 'otro']
        for i, seniority in enumerate(seniority_values):
            job = JobOffer(
                title= "Full Stack Developer",
                company = "Tech Company",
                url = f"https://example.com/job/{i+1}",
                seniority = seniority
            ).save()
            assert job.seniority == seniority

        with pytest.raises(Exception):
            JobOffer(
                title= "Full Stack Developer",
                company = "Tech Company",
                url = "https://example.com/job/2",
                seniority = "invalid_choice"
            ).save()


    def test_str_representation(self):
        job = JobOffer(
            title="Full Stack Developer",
            company="Tech Company",
            image="https://example.com/logo.png",
            location="Remote",
            movility="Yes",
            salary=60000.0,
            description="We are looking for a Full Stack Developer...",
            url="https://example.com/job/1",
            skills=["Python", "Django", "React"],
            experience_required="2 years",
            seniority="mid",
            type_contract="Full-time"
        ).save()
        assert str(job) == 'Full Stack Developer, Tech Company'