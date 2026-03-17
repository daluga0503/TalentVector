from rest_framework import serializers

class ScrapingResultSerialzer(serializers.Serializer):
    total_scrapped = serializers.IntegerField()
    saved = serializers.IntegerField()
    skipped =serializers.IntegerField()