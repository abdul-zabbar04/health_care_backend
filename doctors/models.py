from django.db import models
from accounts.models import Patient, Doctor

from django.db import models
from django.utils.timezone import now

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
    ]

    TIME_SLOTS = [
        ('09:00 AM', '09:00 AM'),
        ('10:00 AM', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('02:00 PM', '02:00 PM'),
        ('03:00 PM', '03:00 PM'),
        ('04:00 PM', '04:00 PM'),
    ]

    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=10, choices=TIME_SLOTS, null=True, blank=True)  # Time slot selection
    reason = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    is_paid = models.BooleanField(default=False)
    meeting_link= models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically fill the meeting link from the selected doctor's link
        if not self.meeting_link and self.doctor and self.doctor.meeting_link:
            self.meeting_link = self.doctor.meeting_link
            self.fee= self.doctor.fee
        super().save(*args, **kwargs) 

    def __str__(self):
        return f"Appointment: {self.patient.user.email} with {self.doctor.user.email} on {self.appointment_date} at {self.appointment_time}"

    class Meta:
        ordering = ['appointment_date', 'appointment_time', 'created_at']
        unique_together = ('patient', 'appointment_date', 'appointment_time')  # Prevent duplicate time slots for same patient


# Review Model

REVIEWSTAR=[
    ("★","★"),
    ("★★","★★"),
    ("★★★","★★★"),
    ("★★★★","★★★★"),
    ("★★★★★","★★★★★"),
]

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor", null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient', null=True, blank=True)
    patient_full_name = models.CharField(max_length=100, null=True, blank=True)
    rating = models.CharField(max_length=10, choices=REVIEWSTAR)
    body = models.TextField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Automatically set the full name of the patient before saving
        self.patient_full_name = f"{self.patient.user.first_name} {self.patient.user.last_name}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Return full name dynamically in __str__ method
        return f"{self.patient.user.first_name} reviewed {self.doctor.user.first_name}"
