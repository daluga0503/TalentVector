import pytest
from django.contrib.auth import get_user_model
from app.users.services import register_user, get_all_users

User = get_user_model()

@pytest.mark.django_db
class TestUserService:

    def test_register_user_success(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "John",
            "surname": "Doe",
            "password": "securepass123"
        }

        user = register_user(data)
        assert user.pk is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.name == "John"
        assert user.surname == "Doe"
        assert user.check_password("securepass123")

    def test_register_user_hash_password(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "John",
            "surname": "Doe",
            "password": "securepass123"
        }

        user = register_user(data)
        assert user.password != "securepass123"
        assert user.check_password("securepass123")

    def test_get_all_users(self):
        User.objects.create_user(
            email="test1@example.com",
            username="testuser1",
            name="John",
            surname="Doe",
            password="securepass123"
        )
        User.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            name="Jane",
            surname="Smith",
            password="securepass456"
        )

        users = get_all_users()
        assert len(users) >= 2
        assert users[0].email == "test1@example.com"
        assert users[1].email == "test2@example.com"
        assert users[0].username == "testuser1"
        assert users[1].username == "testuser2"
        assert users[0].name == "John"
        assert users[1].name == "Jane"
        assert users[0].surname == "Doe"
        assert users[1].surname == "Smith"
        assert users[0].check_password("securepass123")
        assert users[1].check_password("securepass456")