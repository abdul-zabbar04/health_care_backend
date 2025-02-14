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
    InitialPayment,
    SuccessPayment,
    FailPayment,
    ReviewView,
    DoctorReviewsListView
)



urlpatterns = [
    path('list/', DoctorListView.as_view(), name='doctor-list'),
    path('list/specialization/<int:specialization_id>/', SpecialistDoctorListView.as_view(), name='specialist-doctor-list'),
    path('list/health_concern/<int:health_concern_id>/', HealthConcernDoctorListView.as_view(), name='health-concern-doctor-list'),
    path('list/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('review/<int:doctor_id>/', ReviewView.as_view(), name='review-create'),
    path('reviews/list/<int:doctor_id>/', DoctorReviewsListView.as_view(), name='review-list'),
]

urlpatterns += [
    path('appointments/', AppointmentListView.as_view(), name='patient-appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='patient-appointment-detail'),
    path('appointments/doctor/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('appointments/doctor/<int:appointment_id>/', DoctorAppointmentCompleteView.as_view(), name='doctor-appointment-complete'),
    path('appointments/payment/<int:appointment_id>/', PaymentView.as_view(), name='payment'),
    path('payment/<int:appointment_id>/', InitialPayment, name='initial-payment'),
    path('payment/<int:appointment_id>/success', SuccessPayment.as_view(), name='success-payment'),
    path('payment/fail/', FailPayment.as_view(), name='fail-payment'),
    path('appointments/create/<int:doctor_id>/', CreateAppointment.as_view(), name='create-appointments'),
    path('appointments/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='appointment-cancel'),
]
