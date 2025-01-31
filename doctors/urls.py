from django.urls import path
from .views import DoctorListView, DoctorDetailView
from .views import (
    AppointmentListView,
    CreateAppointment,
    AppointmentDetailView, 
    DoctorAppointmentsView,
    CancelAppointmentView
)



urlpatterns = [
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('list/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
]

urlpatterns += [
    path('appointments/', AppointmentListView.as_view(), name='patient-appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='patient-appointment-detail'),
    path('appointments/doctor/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('appointments/create/<int:doctor_id>/', CreateAppointment.as_view(), name='create-appointments'),
    path('appointments/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='appointment-cancel'),
]
