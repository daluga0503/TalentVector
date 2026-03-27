from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import (top_companies, top_skills, top_locations, seniority_distribution)

class TopSKillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        return Response(top_skills())


class TopCompaniesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        return Response(top_companies())

class TopLocationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(Self, _):
        return Response(top_locations())

class SeniorityDistributionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, _):
        return Response(seniority_distribution())
