from django.urls import path
from .views import ContactView, NewsletterView

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
]
