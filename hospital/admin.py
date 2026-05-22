from django.contrib import admin
from .models import Patient, Doctor, Appointment, Prescription, Emergency, Ward, Admission


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gender", "phone", "is_inpatient", "is_discharged")
    search_fields = ("name", "phone")
    list_filter = ("is_inpatient", "is_discharged")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = ("get_name", "specialization", "phone")

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    get_name.short_description = "Doctor Name"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "medicine_name")


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ("patient", "emergency_type", "severity", "status")


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ("patient", "ward", "status", "admitted_at")