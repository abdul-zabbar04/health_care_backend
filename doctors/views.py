from accounts.models import Doctor, Patient, ViewCount
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import GetDoctorSerializer, AppointmentSerializer, ReviewSerializer
from rest_framework.exceptions import ValidationError
from .models import Appointment, Review
from accounts.permissions import IsPatient, IsDoctor
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, pagination
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from django.db.models import F




class DoctorListView(APIView):
    serializer_class = GetDoctorSerializer
    
    def get(self, request):
        try:
            # Get the list of doctors with next_verification=True
            doctor_list = Doctor.objects.filter(next_verification=True)
            
            # Create an instance of the paginator
            paginator = pagination.PageNumberPagination()
            paginator.page_size = 8
            # Paginate the queryset based on the request
            paginated_doctors = paginator.paginate_queryset(doctor_list, request)
            
            # Serialize the paginated data
            serializer = GetDoctorSerializer(paginated_doctors, many=True)
            
            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            # If there's any error, return a 204 No Content response
            return Response(status=status.HTTP_204_NO_CONTENT)
    

class SpecialistDoctorListView(APIView):
    serializer_class = GetDoctorSerializer

    def get(self, request, specialization_id):
        try:
            # Filter doctors based on the specialization ID
            doctor_list = Doctor.objects.filter(
                next_verification=True,
                specialization__id=specialization_id
            )

            # Create an instance of the paginator
            paginator = pagination.PageNumberPagination()
            paginator.page_size = 8
            # Paginate the queryset based on the request
            paginated_doctors = paginator.paginate_queryset(doctor_list, request)

            # Serialize the paginated data
            serializer = GetDoctorSerializer(paginated_doctors, many=True)

            # If no doctors are found, return HTTP 204 No Content
            if not paginated_doctors:
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            # In case of error, return HTTP 500 Internal Server Error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthConcernDoctorListView(APIView):
    serializer_class = GetDoctorSerializer

    def get(self, request, health_concern_id):
        try:
            # Filter doctors based on the health concern ID
            doctor_list = Doctor.objects.filter(
                next_verification=True,
                health_concern_id=health_concern_id
            )

            # Create an instance of the paginator
            paginator = pagination.PageNumberPagination()
            paginator.page_size = 8
            # Paginate the queryset based on the request
            paginated_doctors = paginator.paginate_queryset(doctor_list, request)

            # Serialize the paginated data
            serializer = GetDoctorSerializer(paginated_doctors, many=True)

            # If no doctors are found in the paginated result, return HTTP 204 No Content
            if not paginated_doctors:
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            # In case of error, return HTTP 500 Internal Server Error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # If there are multiple IPs, the first one will be the client's real IP
        ip = x_forwarded_for.split(',')[0]
    else:
        # If there's no X-Forwarded-For header, use REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR')
    return ip


class DoctorDetailView(APIView):
    serializer_class = GetDoctorSerializer

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(next_verification=True, pk=pk)
            serializer = GetDoctorSerializer(doctor)

            # Get user or IP for anonymous users
            user = request.user if request.user.is_authenticated else None
            ip_address = get_client_ip(request)
            # Delete records older than 7 days to keep only last week's data
            seven_days_ago = date.today() - timedelta(days=6)
            ViewCount.objects.filter(create_on__lt=seven_days_ago).delete()

            # Ensure unique view count per user or IP per day
            if user:
                view_exists = ViewCount.objects.filter(user=user, doctor=doctor, create_on=date.today()).exists()
            else:
                view_exists = ViewCount.objects.filter(ip_address=ip_address, doctor=doctor, create_on=date.today()).exists()

            if not view_exists:
                view = ViewCount.objects.create(doctor=doctor, create_on=date.today())
                if user:
                    view.user.add(user)  # Add user to ManyToMany field
                else:
                    view.ip_address = ip_address  # Save IP for anonymous users
                    view.save()
                Doctor.objects.filter(next_verification= True, pk=pk).update(total_views=F("total_views") + 1)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"detail": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND) 


# Appointment views start here:
class AppointmentListView(generics.ListAPIView):
    """
    - GET: List all appointments for the logged-in patient.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        """
        Filter appointments for the logged-in patient.
        """
        patient= Patient.objects.get(user= self.request.user)
        return Appointment.objects.filter(patient=patient)

class CreateAppointment(generics.CreateAPIView):
    """
    - POST: Create an appointment for the logged-in patient with a specific doctor.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]  # Ensure the user is a patient

    def perform_create(self, serializer):
        # Get the logged-in user (patient)
        patient = Patient.objects.get(user=self.request.user)

        # Get the doctor from the URL
        doctor = Doctor.objects.get(id=self.kwargs['doctor_id'])

        # Create the appointment
        serializer.save(patient=patient, doctor=doctor)

    def get_queryset(self):
        """
        Optionally, restrict the returned appointments to the logged-in user.
        """
        return Appointment.objects.filter(patient=self.request.user.patient)


class AppointmentDetailView(generics.RetrieveDestroyAPIView):
    """
    - GET: Retrieve details of a specific appointment.
    - DELETE: Cancel the appointment (if allowed).
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        """
        Ensure the patient can only view or delete their own appointments.
        """
        patient= Patient.objects.get(user= self.request.user)
        return Appointment.objects.filter(patient=patient)
    # override the destroy method to add not allow for paid
    def destroy(self, request, *args, **kwargs):
        """
        Add a condition to delete the appointment.
        """
        instance = self.get_object()

        # Condition: Allow deletion only if the appointment is unpaid
        if instance.is_paid:
            return Response(
                {"detail": "You cannot delete a paid appointment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the condition is met, proceed with deletion
        self.perform_destroy(instance)
        return Response(
            {"detail": "Appointment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

class DoctorAppointmentsView(generics.ListAPIView):
    """
    - GET: List all appointments for a specific doctor (Admin/Doctor users).
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        """
        Filter appointments for a specific doctor.
        """
        # doctor_id = self.kwargs.get('doctor_id')
        doctor= Doctor.objects.get(user= self.request.user)
        return Appointment.objects.filter(doctor=doctor, is_paid= True)

# Optional: Cancel Appointment Endpoint (If needed as a separate endpoint)
class CancelAppointmentView(APIView):
    """
    - POST: Cancel an appointment if it is not paid.
    """
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def post(self, request, pk, format=None):
        try:
            patient= Patient.objects.get(user= self.request.user)
            appointment = Appointment.objects.get(pk=pk, patient=patient)
            if appointment.is_paid:
                return Response({"error": "Cannot cancel a paid appointment."}, status=400)
            appointment.is_paid= True
            appointment.status= "Completed"
            appointment.save()
            return Response({"message": "Appointment canceled successfully."}, status=200)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=404)

class DoctorAppointmentCompleteView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request, appointment_id, *args, **kwargs):
        try:
            # Fetch the appointment by ID
            appointment = Appointment.objects.get(id=appointment_id)
            
           
            # Check the current status and update it to 'Completed'
            if appointment.status == 'Confirmed':
                appointment.status = 'Completed'
            else:
                return Response({"detail": "Appointment status is already completed."}, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated appointment
            appointment.save()

            # Return the updated appointment data
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request, appointment_id, *args, **kwargs):
        try:
            # Fetch the appointment by ID
            appointment = Appointment.objects.get(id=appointment_id)        
            # Check the current status and update it to 'Completed'
            if appointment.status == 'Pending':
                appointment.status = 'Confirmed'
                appointment.is_paid= True
                
            elif appointment.status == 'Confirmed':
                return Response({"detail": "Already Paid."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Already completed."}, status=status.HTTP_400_BAD_REQUEST)

            # Return the updated appointment data
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

import uuid

def generate_transaction_id():
    # Generate a unique transaction ID using UUID
    transaction_id = str(uuid.uuid4())
    return transaction_id

from django.shortcuts import redirect
from rest_framework.decorators import api_view


@api_view(['GET'])
def InitialPayment(request, appointment_id):
    try:
        # Get appointment details using the provided appointment_id
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        # If appointment doesn't exist, return an error response
        return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    # SSLCommerz configuration
    settings = {
        'store_id': 'healt67aadebb20d99',  # Store ID for SSLCommerz
        'store_pass': 'healt67aadebb20d99@ssl',  # Store Password for SSLCommerz
        'issandbox': True  # Set to False for live environment
    }
    
    sslcz = SSLCOMMERZ(settings)
    
    post_body = {
        'total_amount': appointment.fee,  # Appointment fee
        'currency': 'BDT',  # Currency
        'tran_id': generate_transaction_id(),  # Unique transaction ID
        'success_url': f"https://health-care-nine-indol.vercel.app/api/doctor/payment/{appointment_id}/success",  # Redirect URL after success
        'fail_url': 'https://health-care-nine-indol.vercel.app/api/doctor/payment/fail/',  # Redirect URL after failure
        'cancel_url': 'https://health-care-nine-indol.vercel.app/api/doctor/payment/fail/',  # Redirect URL after cancel
        'emi_option': 0,
        'cus_name': f"{appointment.patient.user.first_name} {appointment.patient.user.last_name}",  # Patient's full name
        'cus_email': appointment.patient.user.email,  # Patient's email
        'cus_phone': "01700000000",  
        'cus_add1': "customer address",  
        'cus_city': "Dhaka",  
        'cus_country': "Bangladesh",  
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Doctor Appointment",  
        'product_category': "Test Category",  
        'product_profile': "general" 
    }
    response = sslcz.createSession(post_body)
    return Response({"GatewayPageURL": response['GatewayPageURL']}, status=status.HTTP_200_OK)

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, HttpResponseRedirect


@method_decorator(csrf_exempt, name='dispatch')
class SuccessPayment(APIView):
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
                    
        if appointment.status == 'Pending':
            appointment.status = 'Confirmed'
            appointment.is_paid = True
            
            # For tracking doctor balance
            appointed_doctor = appointment.doctor.id
            doctor= Doctor.objects.get(id= appointed_doctor)
            print("This is docccccccccccccccccccccccccccctor", doctor)
            # Safely update total_appointments and financial fields
            doctor.total_appointments = F('total_appointments') + 1
            doctor.total_earned = F('total_earned') + appointment.fee
            doctor.current_balance = F('current_balance') + appointment.fee
            print(appointed_doctor, doctor.total_earned, "shtgs............................................")
            doctor.save(update_fields=['total_appointments', 'total_earned', 'current_balance'])
            print(doctor.current_balance, doctor.total_earned, appointment.fee)
            appointment.save()
            doctor.save()
            print(doctor)

            appointment.save()
            serializer = AppointmentSerializer(appointment)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            frontend_url = f'https://smart-health-care-web.netlify.app/payment-success/{appointment.id}'  # Example URL, adjust as needed
            return HttpResponseRedirect(frontend_url)

        elif appointment.status == 'Confirmed':
            return Response({"detail": "Already Paid."}, status=status.HTTP_400_BAD_REQUEST)
        
        fail_page= 'https://smart-health-care-web.netlify.app/payment-fail'
        HttpResponseRedirect(fail_page)
        # return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)



class FailPayment(APIView):
    def post(self, request):
        print(id)
        # Define the redirect URL
        fail_page = 'https://smart-health-care-web.netlify.app/payment-fail'

        # Return an HTTP response that redirects the user to the fail page
        return HttpResponseRedirect(fail_page)
    
# Review View
class ReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]  # Ensure the user is a patient

    def perform_create(self, serializer):
        # Get the logged-in user (patient)
        # patient = Patient.objects.get(user=self.request.user)
        patient = get_object_or_404(Patient, user=self.request.user)

        # Get the doctor from the URL
        # doctor = Doctor.objects.get(id=self.kwargs['doctor_id'])
        doctor = get_object_or_404(Doctor, id=self.kwargs['doctor_id'])
        doctor.total_comments= Review.objects.filter(doctor= doctor).count()
        doctor.save()
        # Create the appointment
        serializer.save(patient=patient, doctor=doctor)

# Doctor review list
class DoctorReviewsListView(generics.ListAPIView):
    """
    - GET: List all reviews for a specific doctor (Admin/Doctor users).
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Filter reviews for a specific doctor based on doctor id which is get from url.
        """
        doctor = get_object_or_404(Doctor, id=self.kwargs['doctor_id'])
        return Review.objects.filter(doctor=doctor)
