from django.shortcuts import render
from django.contrib.auth import get_user_model

from patients.models import Patient
from appointments.models import Appointment
from pharmacy.models import Prescription

User = get_user_model()


def admin_dashboard(request):

    patients_count = Patient.objects.count()
    doctors_count = User.objects.count()
    appointments_count = Appointment.objects.count()
    prescriptions_count = Prescription.objects.count()

    return render(request, 'admin/dashboard.html', {
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'prescriptions_count': prescriptions_count,
    })