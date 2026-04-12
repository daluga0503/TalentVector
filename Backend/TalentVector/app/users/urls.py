from django.urls import path
from .views import RegisterView, CustomTokenView, ProfileView, UserListView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/users/', UserListView.as_view(), name='users'),
]