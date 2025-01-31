from django.urls import path
from .views import SpecializationView

urlpatterns = [
    path("specialization/", SpecializationView.as_view(), name="specialization")
]
