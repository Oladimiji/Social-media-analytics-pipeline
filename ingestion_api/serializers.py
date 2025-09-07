# ingestion_api/serializers.py
from rest_framework import serializers

class SocialMediaPostSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()