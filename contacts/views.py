from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import ContactSerializer, NewsletterSerializer

# Create your views here.
class ContactView(CreateAPIView):
    serializer_class= ContactSerializer

class NewsletterView(CreateAPIView):
    serializer_class= NewsletterSerializer
    