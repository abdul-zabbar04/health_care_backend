from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
import re
from filterings.models import Specialization, District, Sub_district, HealthConcern

# Create your models here.

class CustomUser(AbstractUser):
    ROLES= (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('hospital', 'Hospital')
    )
    role= models.CharField(max_length=10, choices=ROLES, null=True, blank=True)
    email = models.EmailField(unique=True)
    # profile_image= models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default.png')
    profile_image = models.URLField(max_length=500, blank=True, null=True, default="https://i.ibb.co.com/0R4xM5rk/default.png")
    # Ensure email is used for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Ensure superuser's role is always None
        if self.is_superuser:
            self.role = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class Patient(models.Model):
    HEIGHT= ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)

    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    height_ft= models.IntegerField(choices=HEIGHT, null=True, blank=True)
    height_in= models.IntegerField(choices=HEIGHT, null=True, blank=True)
    weight_kg= models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email

# meeting link validation
def validate_meeting_link(value):
    if not re.match(r'https?://(zoom\.us|meet\.google\.com)/', value):
        raise ValidationError("Invalid meeting link. Only Zoom or Google Meet links are allowed.")

class Doctor(models.Model):
    DAYS_OF_WEEK = [
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    BMDC_number = models.CharField(max_length=100, null=True, blank=True)
    degrees = models.CharField(max_length=100, null=True, blank=True)
    specialization= models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True, blank=True)
    health_concern= models.ForeignKey(HealthConcern, on_delete=models.CASCADE, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    experience= models.IntegerField(null=True, blank=True)
    # patient_checked= models.IntegerField(null=True, blank=True)
    hospital_name= models.CharField(max_length=50, null=True, blank=True)
    # working_days= MultiSelectField(choices=DAYS_OF_WEEK, null=True, blank=True)
    district= models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    sub_district= models.ForeignKey(Sub_district, on_delete=models.CASCADE, blank=True, null=True)
    region= models.CharField(max_length=50, null=True, blank=True)
    biography= models.TextField(max_length=300, null=True, blank=True)
    meeting_link = models.URLField(
    max_length=500,
    blank=True,
    null=True,
    validators=[validate_meeting_link],
    help_text="Meeting link (Zoom or Google Meet only)")
    next_verification= models.BooleanField(default=False)
    total_views= models.PositiveIntegerField(default=0, null=True, blank=True)
    total_earned= models.PositiveIntegerField(default=0, null=True, blank=True)
    current_balance= models.PositiveIntegerField(default=0, null=True, blank=True)
    total_comments= models.PositiveIntegerField(default=0, null=True, blank=True)
    total_appointments= models.PositiveIntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return self.user.email
    
class ViewCount(models.Model):
    user = models.ManyToManyField(CustomUser, blank=True)  # Multiple users can view a doctor
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="view_count")
    create_on = models.DateField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # For storing IP addresses of anonymous users

    def __str__(self):
        # Displaying the email of the first user in the view count, if exists
        return f"{self.user.first().email if self.user.exists() else self.ip_address} viewed {self.doctor.user.email}"



class Hospital(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='hospital_profile')
    address = models.TextField()
    number_of_departments = models.IntegerField()
    
    def __str__(self):
        return self.user.email
    
