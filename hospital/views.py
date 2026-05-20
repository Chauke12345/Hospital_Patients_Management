from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import request
from .models import Emergency, Patient, Doctor, Appointment, Prescription



# =========================
# DASHBOARD
# =========================
def dashboard(request):
    patients = Patient.objects.all()

    return render(request, "hospital/dashboard.html", {
        "patients": patients,
        "total_patients": patients.count(),
        "admitted": Patient.objects.filter(is_inpatient=True).count(),
        "discharged": Patient.objects.filter(is_discharged=True).count(),
    })


# =========================
# PATIENT LIST
# =========================
def patient_list(request):
    patients = Patient.objects.all().order_by("-created_at")

    return render(request, "hospital/patient_list.html", {
        "patients": patients
    })


# =========================
# DOCTOR LIST
# =========================
def doctor_list(request):
    doctors = Doctor.objects.all()

    return render(request, "hospital/doctor_list.html", {
        "doctors": doctors
    })


# =========================
# DISCHARGE PATIENT
# =========================
def discharge_patient(request, pk):
    patient = get_object_or_404(Patient, id=pk)

    patient.is_discharged = True
    patient.is_inpatient = False
    patient.save()

    return redirect("dashboard")


# =========================
# RECEPTION
# =========================
def reception(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient_id")
        doctor_id = request.POST.get("doctor")

        if not doctor_id:
            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "patients": patients,
                "error": "Please select a doctor"
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        else:
            patient = Patient()
            patient.is_inpatient = True

        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.ward = request.POST.get("ward")
        patient.reason = request.POST.get("reason")
        patient.priority = request.POST.get("priority")
        patient.doctor = doctor

        patient.save()

        return redirect("reception")

    return render(request, "hospital/reception.html", {
        "doctors": doctors,
        "patients": patients
    })


# =========================
# DOCTOR DASHBOARD
# =========================
def doctor_dashboard(request):
    appointments = Appointment.objects.all()

    return render(request, "doctor/dashboard.html", {
        "appointments": appointments
    })


def appointments_list(request):

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()

    # HANDLE FORM SUBMISSION
    if request.method == "POST":

        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        if not patient_id or not doctor_id:
            return render(request, "hospital/appointments.html", {
                "patients": patients,
                "doctors": doctors,
                "appointments": appointments,
                "error": "Please select both patient and doctor"
            })

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            reason=request.POST.get("reason")
        )

        return redirect("appointments_list")

    # LOAD PAGE (GET REQUEST)
    return render(request, "hospital/appointments.html", {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments
    })

# =========================
# CREATE PRESCRIPTION
# =========================
def create_prescription(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        # ✅ VALIDATION
        if not patient_id or not doctor_id:
            return render(request, "hospital/prescriptions.html", {
                "patients": patients,
                "doctors": doctors,
                "error": "Please select both patient and doctor"
            })

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Prescription.objects.create(
            patient=patient,
            doctor=doctor,
            medicine_name=request.POST.get("medicine_name"),
            dosage=request.POST.get("dosage"),
            instructions=request.POST.get("instructions")
        )

        return redirect("prescriptions_list")

    return render(request, "hospital/create_prescription.html", {
        "patients": patients,
        "doctors": doctors
    })
# =========================
# PRESCRIPTION LIST
# =========================
def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by("-id")

    return render(request, "hospital/prescription_list.html", {
        "prescriptions": prescriptions
    })


# =========================
# EDIT PATIENT
# =========================
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.condition = request.POST.get("condition")
        patient.save()
        return redirect("patients_list")

    return render(request, "hospital/edit_patient.html", {
        "patient": patient
    })

def delete_appointment(request, id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=id)
        appointment.delete()
    return redirect('appointments_list')

def edit_prescription(request, id):
    prescription = Prescription.objects.get(id=id)

    if request.method == "POST":
        prescription.medicine_name = request.POST['medicine_name']
        prescription.dosage = request.POST['dosage']
        prescription.instructions = request.POST['instructions']
        prescription.save()

        return redirect('prescriptions_list')

    return render(request, 'hospital/edit_prescription.html', {
        'prescription': prescription
    })

def emergency_list(request):
    emergencies = Emergency.objects.all().order_by('-created_at')
    return render(request, 'hospital/emergency_list.html', {
        'emergencies': emergencies
    })

def create_emergency(request):
    patients = Patient.objects.all()

    if request.method == "POST":
        Emergency.objects.create(
            patient_id=request.POST['patient'],
            emergency_type=request.POST['emergency_type'],
            severity=request.POST['severity'],
            description=request.POST['description'],
        )
        return redirect('emergency_list')

    return render(request, 'hospital/create_emergency.html', {
        'patients': patients
    })

def edit_emergency(request, id):
    emergency = Emergency.objects.get(id=id)

    if request.method == "POST":
        emergency.emergency_type = request.POST['emergency_type']
        emergency.severity = request.POST['severity']
        emergency.description = request.POST['description']
        emergency.status = request.POST['status']
        emergency.save()

        return redirect('emergency_list')

    return render(request, 'hospital/edit_emergency.html', {
        'emergency': emergency
    })
