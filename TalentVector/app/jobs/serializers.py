from rest_framework import serializers

class JobOfferSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    company = serializers.CharField()
    image = serializers.CharField()
    location = serializers.CharField(required=False, allow_blank=True)
    movility = serializers.CharField(required=False, allow_null=True)
    salary = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False)
    url = serializers.CharField()
    skills = serializers.ListField(
        child = serializers.CharField(),
        required=False
    )
    experience_required = serializers.CharField(required=False, allow_blank=True)
    seniority = serializers.CharField(required=False, allow_blank=True)
    type_contract = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
