from rest_framework import serializers
from accounts.models import CustomUser, Doctor, Patient
from .models import Appointment
from django.utils.timezone import now



# For getting user details in doctor or patient or hospital
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields= ['username', 'first_name', 'last_name', 'email', 'profile_image', 'last_login', 'date_joined']

class GetDoctorSerializer(serializers.ModelSerializer):
    # working_days = serializers.ListField(
    #     child=serializers.CharField(max_length=10),
    #     allow_empty=False
    # ) # to handle list type input
    user= UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'
        depth=1


# Appointment Section:
class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'reason', 'status', 'is_paid', 'medical_report']
        read_only_fields = ['status', 'is_paid']

    def validate(self, data):
        # Ensure the appointment date is not in the past
        if data['appointment_date'] < now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
        # Check for conflicts (e.g., existing appointment at the same time)
        if Appointment.objects.filter(
            patient=data['patient'], 
            doctor=data['doctor'], 
            appointment_date=data['appointment_date']
        ).exists():
            raise serializers.ValidationError("This appointment already exists.")
        return data
    
    def validate_medical_report(self, value):
        max_file_size = 2 * 1024 * 1024  # 2 MB
        if value:
            if value.size > max_file_size:
                raise serializers.ValidationError("The uploaded file exceeds the size limit of 2 MB.")
            if not value.name.endswith('.pdf'):
                raise serializers.ValidationError("Only PDF files are allowed for the medical report.")
        return value
