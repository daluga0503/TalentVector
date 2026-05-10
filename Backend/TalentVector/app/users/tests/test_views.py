import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()



@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def __create_user(email="test@example.com", username="testuser", name="John", surname="Doe", password="securepass123"):
        return User.objects.create_user(
            email=email,
            username=username,
            name=name,
            surname=surname,
            password=password
        )
    return __create_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    response = api_client.post('/api/auth/login/',{
        "email": "test@example.com",
        "password": "securepass123"
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client, user

@pytest.mark.django_db
class TestRegisterView:

    def test_register_success(self, api_client):
        response = api_client.post('/api/auth/register/', {
            'email': 'new@example.com',
            'username': 'newuser',
            'name': 'New',
            'surname': 'User',
            'password': 'newpass123'
        })
        assert response.status_code == 201
        assert response.data['email'] == 'new@example.com'

    def test_register_duplicate_email(self, api_client, create_user):
        create_user(email='dup@example.com')
        response = api_client.post('/api/auth/register/', {
            'email': 'dup@example.com',
            'username': 'other',
            'name': 'Dup',
            'surname': 'User',
            'password': 'pass123'
        })
        assert response.status_code == 400

    def test_register_missing_fields(self, api_client):
        response = api_client.post('/api/auth/register/', {'email': 'only@example.com'})
        assert response.status_code == 400


@pytest.mark.django_db
class TestLoginView:

    def test_login_success(self, api_client, create_user):
        create_user()
        response = api_client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'securepass123'
        })
        print("\n", response.data)  # <-- añade esto
        assert response.status_code == 200

    def test_login_wrong_password(self, api_client, create_user):
        create_user()
        response = api_client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpass'
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post('/api/auth/login/', {
            'email': 'ghost@example.com',
            'password': 'pass123'
        })
        assert response.status_code == 401

@pytest.mark.django_db
class TestProfileView:

    def test_profile_authenticated(self, auth_client):
        client, user = auth_client
        response = client.get('/api/auth/profile/')
        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_profile_unauthenticated(self, api_client):
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == 401

@pytest.mark.django_db
class TestUserListView:

    def test_list_authenticated(self, auth_client):
        client, _ = auth_client
        response = client.get('/api/auth/users/')
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_list_unauthenticated(self, api_client):
        response = api_client.get('/api/auth/users/')
        assert response.status_code == 401