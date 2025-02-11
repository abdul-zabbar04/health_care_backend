from accounts.models import Doctor, Patient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import GetDoctorSerializer, AppointmentSerializer
from rest_framework.exceptions import ValidationError
from .models import Appointment
from accounts.permissions import IsPatient, IsDoctor
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions



class DoctorListView(APIView):
    serializer_class= GetDoctorSerializer
    
    def get(self, request):
        try:
            doctor_list= Doctor.objects.filter(next_verification= True)
            serializer= GetDoctorSerializer(doctor_list, many= True)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)
    

class SpecialistDoctorListView(APIView):
    serializer_class = GetDoctorSerializer

    def get(self, request, specialization_id):
        try:
            # Filter doctors based on the specialization ID
            doctor_list = Doctor.objects.filter(
                next_verification=True,
                specialization__id=specialization_id
            )

            # Serialize the data
            serializer = GetDoctorSerializer(doctor_list, many=True)

            # If no doctors are found, return HTTP 204 No Content
            if not doctor_list.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.data)

        except Exception as e:
            # In case of error, return HTTP 500 Internal Server Error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthConcernDoctorListView(APIView):
    serializer_class = GetDoctorSerializer

    def get(self, request, health_concern_id):
        try:
            # Filter doctors based on the specialization ID
            doctor_list = Doctor.objects.filter(
                next_verification=True,
                health_concern_id=health_concern_id
            )

            # Serialize the data
            serializer = GetDoctorSerializer(doctor_list, many=True)

            # If no doctors are found, return HTTP 204 No Content
            if not doctor_list.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.data)

        except Exception as e:
            # In case of error, return HTTP 500 Internal Server Error
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class DoctorDetailView(APIView):
    serializer_class= GetDoctorSerializer
    
    def get(self, request, pk):
        try:
            doctor= Doctor.objects.get(next_verification= True, pk= pk)
            serializer= GetDoctorSerializer(doctor)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)
    


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
            
            appointment.save()

            # Return the updated appointment data
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
