from django.urls import path
from .views import FavsJobsView
urlpatterns = [
        path('favsjobs/', FavsJobsView.as_view(), name='favsjobs'),
]