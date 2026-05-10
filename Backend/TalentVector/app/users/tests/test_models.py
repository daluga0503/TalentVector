import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:

    def test_create_user_success(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            name="John",
            surname="Doe",
            password="securepass123"
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.name == "John"
        assert user.surname == "Doe"
        assert user.check_password("securepass123")

    def test_email_is_unique(self):
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            name="John",
            surname="Doe",
            password="securepass123"
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                email="test@example.com",
                username="testuser2",
                name="Jane",
                surname="Smith",
                password="securepass123"
            )
    def test_username_is_unique(self):
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            name="John",
            surname="Doe",
            password="securepass123"
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                email="test2@example.com",
                username="testuser",
                name="Jane",
                surname="Smith",
                password="securepass123"
            )
    def test_str_representation(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            name="John",
            surname="Doe",
            password="securepass123"
        )
        assert str(user) == "John, Doe, test@example.com"