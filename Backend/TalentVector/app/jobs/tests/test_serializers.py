from app.jobs.serializers import JobOfferSerializer

class TestJobOfferSerializer:

    def test_job_offer_serializer_valid_data(self):
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

        serializer = JobOfferSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        job_offer = serializer.save()

        assert job_offer.title == "Full Stack Developer"
        assert job_offer.company == "Tech Company"
        assert job_offer.image == "https://example.com/logo.png"
        assert job_offer.location == "Málaga"
        assert job_offer.movility == "Presencial"
        assert job_offer.salary == 15000
        assert job_offer.description == "Test"
        assert job_offer.url == "https://example.com/job/1"
        assert job_offer.skills == ["Python", "Django", "React"]
        assert job_offer.experience_required == "2 years"
        assert job_offer.seniority == "mid"
        assert job_offer.type_contract == "indefinido"

    def test_missing_requiered_fields(self):
        data = {
            "title": None,
            "company": None,
            "image": "https://example.com/logo.png",
            "location": "Málaga",
            "movility": "Presencial",
            "salary": 15000,
            "description": "Test",
            "url": None,
            "skills": ["Python", "Django", "React"],
            "experience_required": "2 years",
            "seniority": "mid",
            "type_contract": "indefinido"
        }

        serializer = JobOfferSerializer(data=data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors
        assert 'company' in serializer.errors
        assert 'url' in serializer.errors

    def test_optional_fields(self):
        data = {
            "title": "Full Stack Developer",
            "company": "Tech Company",
            "url": "https://example.com/job/1",
        }

        serializer = JobOfferSerializer(data=data)
        assert serializer.is_valid()
        job_offer = serializer.save()
        assert job_offer.title == "Full Stack Developer"
        assert job_offer.company == "Tech Company"
        assert job_offer.url == "https://example.com/job/1"
        assert job_offer.image == None
        assert job_offer.location == None
        assert job_offer.movility == None
        assert job_offer.salary == None
        assert job_offer.description == None
        assert job_offer.skills == []
        assert job_offer.experience_required == None
        assert job_offer.seniority == "junior"
        assert job_offer.type_contract == None