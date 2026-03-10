from rest_framework import serializers

class JobOfferSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    company = serializers.CharField()
    location = serializers.CharField(required=False, allow_blank=True)
    salary = serializers.FloatField(required=False, allow_null=True)
    description = serializers.CharField()
    url = serializers.CharField()
    skills = serializers.ListField(
        child = serializers.CharField(),
        required=False
    )
    seniority = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)