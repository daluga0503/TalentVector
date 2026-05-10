import pytest
from django.contrib.auth import get_user_model
from app.users.serializers import RegisterSerializer, UserListSerializer, UserProfileSerializer

User = get_user_model()

@pytest.mark.django_db
class TestUserRegisterSerializer:

    def test_register_serializer_valid_data(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "John",
            "surname": "Doe",
            "password": "securepass123"
        }

        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.pk is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.name == "John"
        assert user.surname == "Doe"
        assert user.check_password("securepass123")

    def test_password_write_only(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "name": "John",
            "surname": "Doe",
            "password": "securepass123"
        }

        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert 'password' not in serializer.data

    def test_missing_fields(self):
        data = {
            "email": "test@example.com"
        }

        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors
        assert 'name' in serializer.errors
        assert 'surname' in serializer.errors
        assert 'password' in serializer.errors

@pytest.mark.django_db
class TestUserListSerializer:

    def test_user_list_serializer(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            name="John",
            surname="Doe",
            password="securepass123"
        )

        serializer = UserListSerializer(user)
        assert set(serializer.data.keys()) == {'id', 'name', 'surname', 'email', 'username'}
