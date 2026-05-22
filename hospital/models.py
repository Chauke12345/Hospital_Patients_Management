from django.contrib.auth.models import AbstractUser
from django.db import models


# =========================
# USER MODEL
# =========================
class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('RECEPTIONIST', 'Receptionist'),
        ('PHARMACIST', 'Pharmacist'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='RECEPTIONIST'
    )

    def __str__(self):
        return self.username


# =========================
# DOCTOR MODEL
# =========================
class Doctor(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


# =========================
# GENDER CHOICES
# =========================
GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]


# =========================
# WARD MODEL
# =========================
class Ward(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# PATIENT MODEL
# =========================
class Patient(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)

    gender = models.CharField(
        max_length=100,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    phone = models.CharField(max_length=100, null=True, blank=True)

    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reason = models.TextField(null=True, blank=True)

    priority = models.CharField(max_length=100, default="Normal")

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )

    is_inpatient = models.BooleanField(default=False)
    is_discharged = models.BooleanField(default=False)

    admitted_at = models.DateTimeField(null=True, blank=True)
    discharged_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# APPOINTMENT MODEL
# =========================
class Appointment(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")

    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} ({self.date})"


# =========================
# PRESCRIPTION MODEL
# =========================
class Prescription(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('DISPENSED', 'Dispensed'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="prescriptions")

    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    instructions = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.medicine_name}"


# =========================
# EMERGENCY (ED)
# =========================
class Emergency(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emergencies"
    )

    emergency_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)

    description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=50, default="Pending")

    is_admitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.emergency_type}"


# =========================
# ADMISSION MODEL
# =========================
class Admission(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    emergency = models.ForeignKey(
        Emergency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)

    admitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return f"{self.patient.name} - Admission"