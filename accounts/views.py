from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Patient, Doctor, Hospital, CustomUser
from .serializers import PatientProfileSerializer, DoctorProfileSerializer, HospitalProfileSerializer, CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView, ConfirmEmailView
from allauth.account.models import EmailAddress
from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from . import permissions
from allauth.account.views import ConfirmEmailView
from django.db.models import Q
from doctors.models import Appointment

class CustomRegisterView(RegisterView):
    serializer_class= CustomRegisterSerializer
    # here one task is remained that is set the is_active= False. when confirmation link clicked then is_active= True. solve it later

class CustomEmailConfirmView(ConfirmEmailView, APIView):
    def get(self, request, *args, **kwargs):
        try:
            confirmation = self.get_object()
            confirmation.confirm(self.request)
            # Mark the email as verified
            email_address = EmailAddress.objects.get(email=confirmation.email_address.email)
            email_address.verified = True
            email_address.save()

            # Use JsonResponse for proper rendering
            return JsonResponse({"detail": "Email successfully confirmed."}, status=200)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)

class RoleSpecificRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class= DoctorProfileSerializer

    def post(self, request):
        user = request.user
        if user.role == 'patient':
            serializer = PatientProfileSerializer(data=request.data)
        elif user.role == 'doctor':
            serializer = DoctorProfileSerializer(data=request.data)
        elif user.role == 'hospital':
            serializer = HospitalProfileSerializer(data=request.data)
        else:
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"detail": "Profile created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, permissions.IsPatient]

    def get_object(self):
        # Retrieve the profile for the authenticated user
        return Patient.objects.get(user=self.request.user)
    
class DoctorProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, permissions.IsDoctor]

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class HospitalProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = HospitalProfileSerializer
    permission_classes = [IsAuthenticated, permissions.IsHospital] # need to add "is_role==hospital && has Hospital model object"

    def get_object(self):
        return Hospital.objects.get(user=self.request.user)
    
# class UserView(RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user


from dj_rest_auth.views import PasswordResetView
from .serializers import CustomPasswordResetSerializer  # Import your serializer

class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer

from datetime import date, timedelta
from .models import ViewCount
from .serializers import ViewCountStatsSerializer

class ViewCountStatsView(APIView):
    def get(self, request, id):
        today = date.today()
        last_7_days = [today - timedelta(days=i) for i in range(6)]

        # Aggregate the view counts for the last 7 days
        stats = []
        for day in last_7_days:
            views_count = ViewCount.objects.filter(doctor= id, create_on=day).count()
            stats.append({
                "date": day,
                "views_count": views_count
            })

        # Serialize the data
        serializer = ViewCountStatsSerializer(stats, many=True)
        return Response(serializer.data)

from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, timedelta 
from django.shortcuts import get_object_or_404
from .serializers import DailyIncomeStatsSerializer
from .models import Doctor


class DailyIncomeStatsView(APIView):
    def get(self, request, id):
        # Ensure the doctor exists
        doctor = get_object_or_404(Doctor, id=id)

        # Get the last 7 days (including today)
        today = date.today()  
        last_7_days = [today - timedelta(days=i) for i in range(6)]  

        stats = []

        for day in last_7_days:
            daily_income = (
                Appointment.objects.filter(
                    doctor=id,
                    is_paid=True,
                    created_at__date=day
                ).aggregate(total_income=Sum('fee'))['total_income'] or 0
            )

            # Ensure we don't double-count if created_at and updated_at are the same
            updated_income = (
                Appointment.objects.filter(
                    doctor=id,
                    is_paid=True,
                    updated_at__date=day
                )
                .exclude(created_at__date=day)  
                .aggregate(total_income=Sum('fee'))['total_income'] or 0
            )

            total_income = daily_income + updated_income
            stats.append({"date": day, "income": total_income})

        print(stats)  # Debugging, remove in production

        # Serialize and return response
        serializer = DailyIncomeStatsSerializer(stats, many=True)
        return Response({"doctor_id": id, "income_stats": serializer.data})



