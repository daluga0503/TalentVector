from .views import JobListCreateView, JobDetailView
from django.urls import path

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='jobs'),
    path('jobs/<int:job_id>/', JobDetailView.as_view(), name='job-detail')
]