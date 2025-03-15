from django.urls import path
from .views import (
    RoleSpecificRegistrationView,
    PatientProfileView,
    DoctorProfileView,
    HospitalProfileView,
    ViewCountStatsView,
    DailyIncomeStatsView,
)

urlpatterns = [
    path('register/profile/', RoleSpecificRegistrationView.as_view(), name='role-specific-registration'),
    path('patient-profile/', PatientProfileView.as_view(), name='patient_profile'), # get, edit, delete
    path('doctor-profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('hospital-profile/', HospitalProfileView.as_view(), name='hospital_profile'),
    path('doctor/profile-views/<int:id>/', ViewCountStatsView.as_view(), name='doctor-profile-views'),
    path('doctor/incomes/<int:id>/', DailyIncomeStatsView.as_view(), name='doctor-daily-income'),

]
