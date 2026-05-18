from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from patients.models import Patient
from doctors.models import Doctor


# =========================
# RECEPTION VIEW
# Register New Patient
# =========================
def reception(request):

    doctors = Doctor.objects.all()

    if request.method == 'POST':

        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        ward = request.POST.get('ward')
        reason = request.POST.get('reason')
        priority = request.POST.get('priority')
        doctor_id = request.POST.get('doctor')

        # Validate required fields
        if not name or not age or not doctor_id:
            return render(request, 'hospital/reception.html', {
                'doctors': doctors,
                'error': "Name, Age and Doctor are required"
            })

        # Validate age safely
        try:
            age = int(age)
        except ValueError:
            return render(request, 'hospital/reception.html', {
                'doctors': doctors,
                'error': "Age must be a number"
            })

        # Get selected doctor
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Create patient
        Patient.objects.create(
            name=name,
            age=age,
            gender=gender or "Unknown",
            phone=phone or "",
            ward=ward or "General",
            reason=reason or "",
            priority=priority or "Normal",
            doctor=doctor
        )

        return redirect('patients')

    return render(request, 'hospital/reception.html', {
        'doctors': doctors
    })


# =========================
# ADMIT PATIENT
# =========================
def admit_patient(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    patient.is_inpatient = True
    patient.admitted_at = timezone.now()

    patient.save()

    return redirect('reception_dashboard')