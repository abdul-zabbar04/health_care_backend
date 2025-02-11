from rest_framework import serializers
from .models import Specialization, HealthConcern

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Specialization
        fields= '__all__'

class HealthConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model= HealthConcern
        fields= '__all__'