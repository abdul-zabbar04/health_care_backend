from django.urls import path
from .views import DoctorListView, DoctorDetailView
from .views import (
    AppointmentListView,
    CreateAppointment,
    AppointmentDetailView, 
    DoctorAppointmentsView,
    CancelAppointmentView,
    DoctorAppointmentCompleteView,
    PaymentView,
    SpecialistDoctorListView,
    HealthConcernDoctorListView,
)



urlpatterns = [
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('list/specialization/<int:specialization_id>/', SpecialistDoctorListView.as_view(), name='specialist-doctor-list'),
    path('list/health_concern/<int:health_concern_id>/', HealthConcernDoctorListView.as_view(), name='health-concern-doctor-list'),
    path('list/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
]

urlpatterns += [
    path('appointments/', AppointmentListView.as_view(), name='patient-appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='patient-appointment-detail'),
    path('appointments/doctor/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('appointments/doctor/<int:appointment_id>/', DoctorAppointmentCompleteView.as_view(), name='doctor-appointment-complete'),
    path('appointments/payment/<int:appointment_id>/', PaymentView.as_view(), name='payment'),
    path('appointments/create/<int:doctor_id>/', CreateAppointment.as_view(), name='create-appointments'),
    path('appointments/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='appointment-cancel'),
]
