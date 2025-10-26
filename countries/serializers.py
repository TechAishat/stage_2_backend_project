from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'description', 'population', 'gdp', 'flag_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CountryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'description', 'population', 'gdp', 'flag_image']

class CountryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['description', 'population', 'gdp', 'flag_image']
