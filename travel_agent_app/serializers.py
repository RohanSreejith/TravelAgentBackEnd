from rest_framework import serializers
from .models import TravelAgent, Website, TravelPackage, ScrapedPackage, PackageMedia
from django.contrib.auth import get_user_model

# Use the custom user model
User = get_user_model()


class TravelAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # TravelAgent is your custom user model
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'agency_name']


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'agent', 'name', 'url', 'is_active', 'created_at']


class PackageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageMedia
        fields = ['id', 'media_type', 'file']


class TravelPackageSerializer(serializers.ModelSerializer):
    media = PackageMediaSerializer(many=True, read_only=True)
    agent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TravelPackage
        fields = [
            'id', 'agent', 'title', 'destination', 'duration_days',
            'price', 'description', 'created_at', 'updated_at', 'media'
        ]


class ScrapedPackageSerializer(serializers.ModelSerializer):
    source_website = WebsiteSerializer(read_only=True)
    agent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ScrapedPackage
        fields = [
            'id', 'agent', 'source_website', 'title', 'destination',
            'duration_days', 'price', 'description', 'scraped_at', 'original_url'
        ]
