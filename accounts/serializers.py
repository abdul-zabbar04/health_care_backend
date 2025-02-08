from rest_framework import serializers
from .models import CustomUser, Patient, Doctor, Hospital
from django.core.exceptions import ValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordChangeSerializer, UserDetailsSerializer
from filterings.models import Specialization

class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    def validate_email(self, email):
        # Check if email is already in use
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already exists.")
        return email

    def save(self, request):
        user = super().save(request)
        user.role = self.validated_data['role']
        user.save()
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'height_ft', 'height_in', 'weight_kg']


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['BMDC_number', 'degrees', 'specialization', 'hospital_name', 'experience', 'biography', 'meeting_link']
        depth=1

class HospitalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['address', 'number_of_departments']


from dj_rest_auth.serializers import PasswordChangeSerializer


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The old password is incorrect.")
        return value
    
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= CustomUser
#         fields= ['username', 'first_name', 'last_name', 'email', 'role', 'profile_image']
#         extra_kwargs = {'profile_image': {'required': False}}
#     def update(self, instance, validated_data):
#     # Retain the existing profile image if not provided in the request
#         profile_image = validated_data.get('profile_image', None)
#         if profile_image is None:  # If no new image is uploaded
#             validated_data['profile_image'] = instance.profile_image
#         return super().update(instance, validated_data)

class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        model= CustomUser
        fields= ['first_name', 'last_name', 'email', 'role', 'profile_image']
