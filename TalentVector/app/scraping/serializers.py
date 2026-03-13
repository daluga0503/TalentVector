from rest_framework import serializers

class ScrapingResultSerialzer(serializers.Serializer):
    total_srapped = serializers.IntegerField()
    saved = serializers.IntegerField()
    skiped =serializers.IntegerField()