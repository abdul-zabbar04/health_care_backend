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
        fields = ['id', 'age', 'gender', 'height_ft', 'height_in', 'weight_kg']


class DoctorProfileSerializer(serializers.ModelSerializer):
    specialization_name = serializers.CharField(source='specialization.name', read_only=True)  # Read-only field
    specialization = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())  # Accepts ID
    class Meta:
        model = Doctor
        fields = ['id', 'BMDC_number', 'degrees', 'fee', 'health_concern', 'specialization', 'specialization_name', 'hospital_name', 'experience', 'biography', 'meeting_link', 'total_views', 'total_earned', 'current_balance', 'total_comments', 'total_appointments']
        read_only_fields= ['id', 'total_views', 'total_earned', 'current_balance', 'total_comments', 'total_appointments']

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



# serializers.py
from dj_rest_auth.serializers import PasswordResetSerializer
from django.urls import reverse

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'subject_template_name': 'account/email/password_reset_key_subject.txt',
            'email_template_name': 'account/email/password_reset_key_message.txt',
            'html_email_template_name': 'account/email/password_reset_key_message.html',
            'extra_email_context': {
                'password_reset_url': self.context['request'].build_absolute_uri(
                    reverse('custom_password_reset_confirm', kwargs={'uidb64': 'UID', 'token': 'TOKEN'})  # Placeholder values
                ),
            },
        }

class ViewCountStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    views_count = serializers.IntegerField()

class DailyIncomeStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    income = serializers.IntegerField()
