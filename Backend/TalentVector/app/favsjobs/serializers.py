from models import FavsJobs
from .services import create_favjob, delete_favjob, list_favjobs
from rest_framework import serializers

class FavsJobsSerializer(serializers.ModelSerializer):

    def get_favs_by_user_id(self, validated_data):
        return list_favjobs(**validated_data)

    def create(self, validated_data):
        return create_favjob(**validated_data)
    
    def delete(self, validated_data):
        return delete_favjob(**validated_data)
