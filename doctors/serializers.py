from rest_framework import serializers
from accounts.models import CustomUser, Doctor, Patient
from .models import Appointment, Review
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
from rest_framework import serializers
from django.utils.timezone import now
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    appointment_time = serializers.ChoiceField(choices=Appointment.TIME_SLOTS)  # Time slot selection

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'reason', 'status', 'meeting_link', 'fee', 'is_paid']
        read_only_fields = ['status', 'is_paid', 'meeting_link', 'fee']

    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"

    def validate(self, data):
        # Ensure the appointment date is not in the past
        if data['appointment_date'] < now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        
        # Ensure the appointment is not booked at the same time slot for the same patient
        if Appointment.objects.filter(
            patient=data['patient'], 
            appointment_date=data['appointment_date'], 
            appointment_time=data['appointment_time']
        ).exists():
            raise serializers.ValidationError("You already have an appointment at this time slot.")

        return data

    
    # def validate_medical_report(self, value):
    #     max_file_size = 2 * 1024 * 1024  # 2 MB
    #     if value:
    #         if value.size > max_file_size:
    #             raise serializers.ValidationError("The uploaded file exceeds the size limit of 2 MB.")
    #         if not value.name.endswith('.pdf'):
    #             raise serializers.ValidationError("Only PDF files are allowed for the medical report.")
    #     return value


class ReviewSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    class Meta:
        model= Review
        fields= ['doctor', 'patient', 'patient_full_name', 'rating', 'body', 'created_on']
        read_only_fields= ['patient_full_name', 'created_on']