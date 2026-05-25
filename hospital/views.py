from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Emergency,
    Patient,
    Doctor,
    Appointment,
    Prescription,
    Admission,
    Ward,
)

# =========================
# DASHBOARD
# =========================
def dashboard(request):
    return render(request, "hospital/dashboard.html", {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "emergency_count": Emergency.objects.count(),
    })
# =========================
# PATIENTS
# =========================
def patient_list(request):
    patients = Patient.objects.all().order_by("-created_at")
    return render(request, "hospital/patient_list.html", {"patients": patients})


def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.condition = request.POST.get("condition")
        patient.save()
        return redirect("patient_list")

    return render(request, "hospital/edit_patient.html", {"patient": patient})


def discharge_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.is_discharged = True
    patient.is_inpatient = False
    patient.save()
    return redirect("dashboard")


# =========================
# DOCTORS
# =========================
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "hospital/doctor_list.html", {"doctors": doctors})


def doctor_dashboard(request):
    appointments = Appointment.objects.select_related("patient", "doctor")
    return render(request, "doctor/dashboard.html", {"appointments": appointments})


# =========================
# RECEPTION
# =========================
def reception(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient_id")

        if not doctor_id:
            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "patients": patients,
                "error": "Please select a doctor"
            })

        doctor = get_object_or_404(Doctor, pk=doctor_id)
        patient = get_object_or_404(Patient, pk=patient_id) if patient_id else Patient()

        patient.name = request.POST.get("name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.ward = Ward.objects.get(name=request.POST.get("ward"))
        patient.reason = request.POST.get("reason")
        patient.priority = request.POST.get("priority")
        patient.doctor = doctor
        patient.is_inpatient = True
        patient.save()

        return redirect("reception")

    return render(request, "hospital/reception.html", {
        "doctors": doctors,
        "patients": patients
    })


# =========================
# APPOINTMENTS
# =========================
def appointments_list(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()

    if request.method == "POST":
        Appointment.objects.create(
            patient=get_object_or_404(Patient, pk=request.POST.get("patient")),
            doctor=get_object_or_404(Doctor, pk=request.POST.get("doctor")),
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            reason=request.POST.get("reason"),
        )
        return redirect("appointments_list")

    return render(request, "hospital/appointments.html", {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments
    })


def delete_appointment(request, id):
    if request.method == "POST":
        get_object_or_404(Appointment, id=id).delete()
    return redirect("appointments_list")


# =========================
# PRESCRIPTIONS
# =========================
def create_prescription(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == "POST":
        Prescription.objects.create(
            patient=get_object_or_404(Patient, pk=request.POST.get("patient")),
            doctor=get_object_or_404(Doctor, pk=request.POST.get("doctor")),
            medicine_name=request.POST.get("medicine_name"),
            dosage=request.POST.get("dosage"),
            instructions=request.POST.get("instructions"),
        )
        return redirect("prescriptions_list")

    return render(request, "hospital/create_prescription.html", {
        "patients": patients,
        "doctors": doctors
    })


def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by("-id")
    return render(request, "hospital/prescriptions_list.html", {
        "prescriptions": prescriptions
    })


def edit_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    if request.method == "POST":
        prescription.medicine_name = request.POST.get("medicine_name")
        prescription.dosage = request.POST.get("dosage")
        prescription.instructions = request.POST.get("instructions")
        prescription.save()
        return redirect("prescriptions_list")

    return render(request, "hospital/edit_prescription.html", {
        "prescription": prescription
    })


# =========================
# EMERGENCY
# =========================
def emergency_list(request):
    emergencies = Emergency.objects.all().order_by("-created_at")
    return render(request, "hospital/emergency_list.html", {
        "emergencies": emergencies
    })


def create_emergency(request):
    doctors = Doctor.objects.all()
    print("CREATE EMERGENCY VIEW HIT")

    if request.method == "POST":
        patient_name = request.POST.get("patient")

        # optional: create or reuse patient
        patient, created = Patient.objects.get_or_create(name=patient_name)

        emergency = Emergency.objects.create(
            patient=patient,
            emergency_type=request.POST.get("emergency_type"),
            severity=request.POST.get("severity"),
            description=request.POST.get("description"),
            status="Pending"
        )

        doctor_id = request.POST.get("doctor")
        if doctor_id:
            emergency.doctor_id = doctor_id
            emergency.save()

        return redirect("emergency_list")

    return render(request, "hospital/create_emergency.html", {
        "doctors": doctors
    })


def edit_emergency(request, id):
    emergency = get_object_or_404(Emergency, id=id)

    if request.method == "POST":
        emergency.emergency_type = request.POST.get("emergency_type")
        emergency.severity = request.POST.get("severity")
        emergency.description = request.POST.get("description")
        emergency.status = request.POST.get("status")
        emergency.save()
        return redirect("emergency_list")

    return render(request, "hospital/edit_emergency.html", {
        "emergency": emergency
    })


# =========================
# ADMISSION
# =========================
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Emergency, Admission, Ward, Doctor


def admit_patient(request, id):
    emergency = get_object_or_404(Emergency, id=id)

    if request.method == "POST":
        Admission.objects.create(
            patient=emergency.patient,
            doctor_id=request.POST.get("doctor"),
            emergency=emergency,
            ward_id=request.POST.get("ward"),
            admitted_at=timezone.now(),
            status="Active",
        )

        emergency.status = "Admitted"
        emergency.save()

        return redirect("emergency_list")

    return render(request, "hospital/reception.html", {
        "emergency": emergency,
        "wards": Ward.objects.all(),
        "doctors": Doctor.objects.all(),
    })
# =========================
# AUTH
# =========================
def signup(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "hospital/signup.html", {"form": form})


def login_view(request):
    error = None

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "hospital/login.html", {"error": error})

from django.shortcuts import get_object_or_404, redirect
from .models import Prescription

def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == "POST":
        prescription.delete()
        return redirect("prescriptions_list")

    return render(request, "hospital/confirm_delete.html", {
        "prescription": prescription
    })

from django import forms
from .models import Emergency

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ["patient", "doctor", "emergency_type", "severity", "description"]

from django.http import Http404

def delete_patient(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return redirect("patient_list")

    if request.method == "POST":
        patient.delete()

    return redirect("patient_list")

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, "hospital/patient_list.html", {"patients": patients})