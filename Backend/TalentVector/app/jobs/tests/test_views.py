import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from app.jobs.models import JobOffer
from app.jobs.services import create_job

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_normal_user():
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="pas123")

@pytest.fixture
def create_admin_user():
    return User.objects.create_superuser(username="admin", email="admin@example.com", password="pass123")

@pytest.mark.django_db
class TestJobsViews:
    def test_get_jobs_authenticated(self, api_client, create_normal_user):
        # Creamos datos previos usando el servicio directamente
        create_job({"title": "Python Dev", "company": "Tech", "url": "url-1"})
        
        # Forzamos la autenticación de usuario normal
        api_client.force_authenticate(user=create_normal_user)
        
        response = api_client.get('/api/jobs/') 
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == "Python Dev"

    def test_get_jobs_unauthenticated_fails(self, api_client):
        # Intentar acceder sin loguearse debe dar 403 Forbidden o 401 Unauthorized
        response = api_client.get('/api/jobs/')
        assert response.status_code in [401, 403]

    def test_get_jobs_with_filters(self, api_client, create_normal_user):
        create_job({"title": "Django Dev", "company": "Alpha", "url": "url-1", "location": "Madrid"})
        create_job({"title": "React Dev", "company": "Beta", "url": "url-2", "location": "Málaga"})
        
        api_client.force_authenticate(user=create_normal_user)
        
        # Probamos pasando query params (?location=Madrid)
        response = api_client.get('/api/jobs/', {'location': 'Madrid'})
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == "Django Dev"

    def test_post_job_as_admin_success(self, api_client, create_admin_user):
        api_client.force_authenticate(user=create_admin_user)
        
        data = {
            "title": "Data Scientist",
            "company": "AI Corp",
            "url": "https://example.com/ai-job"
        }
        
        response = api_client.post('/api/jobs/', data, format='json')
        
        assert response.status_code == 201
        assert response.data['title'] == "Data Scientist"
        assert JobOffer.objects.count() == 1

    def test_post_job_as_create_normal_user_forbidden(self, api_client, create_normal_user):
        api_client.force_authenticate(user=create_normal_user)
        
        data = {"title": "No Admin", "company": "Fail", "url": "fail-url"}
        response = api_client.post('/api/jobs/', data, format='json')
        
        # Un usuario común no puede publicar ofertas
        assert response.status_code == 403

    def test_get_job_detail_success(self, api_client, create_normal_user):
        job = create_job({"title": "Frontend", "company": "Vues", "url": "url-f"})
        api_client.force_authenticate(user=create_normal_user)
        
        response = api_client.get(f'/api/jobs/{job.id}/')
        
        assert response.status_code == 200
        assert response.data['title'] == "Frontend"

    def test_get_job_detail_not_found(self, api_client, create_normal_user):
        api_client.force_authenticate(user=create_normal_user)
        
        # Pasamos un ID inexistente pero válido en longitud para evitar problemas de formato
        response = api_client.get(f'/api/jobs/{"nonexistent_id"}/')
        
        assert response.status_code == 404
        assert response.data['error'] == 'not found'
    