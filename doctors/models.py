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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    is_paid = models.BooleanField(default=False)
    meeting_link= models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically fill the meeting link from the selected doctor's link
        if not self.meeting_link and self.doctor and self.doctor.meeting_link:
            self.meeting_link = self.doctor.meeting_link

    def __str__(self):
        return f"Appointment: {self.patient.user.email} with {self.doctor.user.email} on {self.appointment_date} at {self.appointment_time}"

    class Meta:
        ordering = ['appointment_date', 'appointment_time', 'created_at']
        unique_together = ('patient', 'appointment_date', 'appointment_time')  # Prevent duplicate time slots for same patient
