from django.db import models
from doctors.models import Doctor   # IMPORTANT: single source of truth


class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=100)

    address = models.CharField(max_length=255, null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    priority = models.CharField(max_length=100, default="Normal")
    reason = models.TextField(null=True, blank=True)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )

    admitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name