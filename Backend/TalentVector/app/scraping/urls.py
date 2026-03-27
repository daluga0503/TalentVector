from django.urls import path
from .views import RunScrappingJobs

urlpatterns = [
    path('scraping/run/', RunScrappingJobs.as_view(), name='scrapping-jobs')
]