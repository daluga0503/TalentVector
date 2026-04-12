from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .services import register_user, get_all_users

# Traductor bidireccional entre las instancias de la bbdd y formato json

User = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'username']
        
    def get_all(self):
        return get_all_users()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password', 'username')

    def create(self, validated_data):
        return register_user(validated_data)
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token['email'] = user.email
        token['name'] = user.name
        token['surname'] = user.surname

        return token
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'username', 'date_joined', 'is_staff']
        read_only_fields = ['date_joined', 'is_staff']