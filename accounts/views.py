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