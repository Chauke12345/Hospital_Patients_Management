from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Patient
from .forms import PatientForm


# =========================
# PATIENT LIST
# =========================
@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')

    return render(request, 'patients/patient_list.html', {
        'patients': patients
    })


# =========================
# ADD PATIENT
# =========================
@login_required
def add_patient(request):
    form = PatientForm()

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')

    return render(request, 'patients/add_patient.html', {
        'form': form
    })


# =========================
# DISCHARGE PATIENT
# =========================
@login_required
def discharge_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        patient.is_discharged = True
        patient.discharged_at = timezone.now()
        patient.save()

    return redirect('patient_list')