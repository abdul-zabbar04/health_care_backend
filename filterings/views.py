from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import SpecializationSerializer
from .models import Specialization

class SpecializationView(ListAPIView):
    serializer_class= SpecializationSerializer
    queryset= Specialization.objects.all()