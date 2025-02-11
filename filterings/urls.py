from django.urls import path
from .views import SpecializationView, HealthConcernView

urlpatterns = [
    path("specialization/", SpecializationView.as_view(), name="specialization"),
    path("health_concern/", HealthConcernView.as_view(), name="health_concern"),
]
