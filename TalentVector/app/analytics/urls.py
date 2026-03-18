from django.urls import path
from .views import (TopCompaniesView, TopLocationsView, TopSKillsView, SeniorityDistributionView)


urlpatterns = [
    path('stats/top-skills/', TopSKillsView.as_view(), name='Top Skills'),
    path('stats/top-companies/', TopCompaniesView.as_view(), name='Top Companies'),
    path('stats/top-locations/', TopLocationsView.as_view(), name='Top Locations'),
    path('stats/seniority-distribution', SeniorityDistributionView.as_view(), name='Seniority Distribution')
]