from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import ContactSerializer

# Create your views here.
class ContactView(CreateAPIView):
    serializer_class= ContactSerializer
    