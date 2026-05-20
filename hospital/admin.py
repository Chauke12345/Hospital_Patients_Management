from django.contrib import admin
from .models import User, Appointment, Prescription, Doctor, Patient

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Doctor)
admin.site.register(Patient)