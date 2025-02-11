from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import SpecializationSerializer, HealthConcernSerializer
from .models import Specialization, HealthConcern

class SpecializationView(ListAPIView):
    serializer_class= SpecializationSerializer
    queryset= Specialization.objects.all()

class HealthConcernView(ListAPIView):
    serializer_class= HealthConcernSerializer
    queryset= HealthConcern.objects.all()