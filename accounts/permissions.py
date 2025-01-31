from rest_framework.permissions import BasePermission
from allauth.account.models import EmailAddress
from . import models
from rest_framework.exceptions import PermissionDenied

class IsPatient(BasePermission):
    """
    Allows access only to users with the 'patient' role and verified email,
    and requires role-based registration.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.role != 'patient':
            raise PermissionDenied("You must be a patient to access this resource.")
        try:
            email_address = EmailAddress.objects.get(user=user)
            if not email_address.verified:
                raise PermissionDenied("Your email address must be verified.")
        except EmailAddress.DoesNotExist:
            raise PermissionDenied("Email address not found.")
        try:
            # Check if the user has a patient profile
            models.Patient.objects.get(user=user)
        except models.Patient.DoesNotExist:
            raise PermissionDenied("You must complete your patient profile registration.")
        return True


class IsDoctor(BasePermission):
    """
    Allows access only to users with the 'doctor' role and verified email,
    and requires role-based registration.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.role != 'doctor':
            raise PermissionDenied("You must be a doctor to access this resource.")
        try:
            email_address = EmailAddress.objects.get(user=user)
            if not email_address.verified:
                raise PermissionDenied("Your email address must be verified.")
        except EmailAddress.DoesNotExist:
            raise PermissionDenied("Email address not found.")
        try:
            # Check if the user has a patient profile
            models.Doctor.objects.get(user=user)
        except models.Doctor.DoesNotExist:
            raise PermissionDenied("You must complete your doctor profile registration.")
        return True


class IsHospital(BasePermission):
    """
    Allows access only to users with the 'hospital' role and verified email,
    and requires role-based registration.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.role != 'hospital':
            raise PermissionDenied("You must be a hospital to access this resource.")
        try:
            email_address = EmailAddress.objects.get(user=user)
            if not email_address.verified:
                raise PermissionDenied("Your email address must be verified.")
        except EmailAddress.DoesNotExist:
            raise PermissionDenied("Email address not found.")
        try:
            # Check if the user has a patient profile
            models.Hospital.objects.get(user=user)
        except models.Hospital.DoesNotExist:
            raise PermissionDenied("You must complete your hospital profile registration.")
        return True
