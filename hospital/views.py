from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# =========================
# IMPORT MODELS
# =========================
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from pharmacy.models import Prescription



# =========================
# LOGIN VIEW
# =========================
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Please enter username and password"
        else:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("dashboard")

            error = "Invalid username or password"

    return render(request, "hospital/login.html", {"error": error})


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# DASHBOARD VIEW
# =========================
def dashboard(request):
    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "total_prescriptions": Prescription.objects.count(),
    }
    return render(request, "hospital/dashboard.html", context)


# =========================
# PATIENT LIST VIEW
# =========================
def patient_list(request):
    patients = Patient.objects.all().order_by("-id")
    return render(request, "hospital/patients.html", {"patients": patients})


# =========================
# RECEPTION (REGISTER PATIENT)
# =========================
from django.shortcuts import render, redirect
from .models import Doctor, Patient
import traceback

def reception(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            age = request.POST.get("age")
            doctor_id = request.POST.get("doctor")

            # Validate doctor
            try:
                doctor = Doctor.objects.get(id=doctor_id)
            except Doctor.DoesNotExist:
                return render(request, "hospital/reception.html", {
                    "doctors": doctors,
                    "error": "Invalid doctor selected"
                })

            # Validate age
            try:
                age = int(age)
            except (ValueError, TypeError):
                return render(request, "hospital/reception.html", {
                    "doctors": doctors,
                    "error": "Age must be a valid number"
                })

            # Create patient
            Patient.objects.create(
                name=name,
                age=age,
                gender=request.POST.get("gender") or "Not specified",
                phone=request.POST.get("phone") or "",
                ward=request.POST.get("ward") or "General",
                reason=request.POST.get("reason") or "",
                priority=request.POST.get("priority") or "Normal",
                doctor=doctor
            )

            return redirect("patients")

        except Exception as e:
            print("RECEPTION ERROR:", e)
            print(traceback.format_exc())

            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Something went wrong while saving patient"
            })

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })

# =========================
# APPOINTMENTS VIEW
# =========================
def appointments(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    appointments_list = Appointment.objects.all().order_by("-created_at")

    if request.method == "POST":
        try:
            doctor_id = request.POST.get("doctor")
            patient_id = request.POST.get("patient")
            date = request.POST.get("date")
            time = request.POST.get("time")
            reason = request.POST.get("reason", "")

            if not all([doctor_id, patient_id, date, time]):
                raise ValueError("Missing required fields")

            doctor = Doctor.objects.get(id=int(doctor_id))
            patient = Patient.objects.get(id=int(patient_id))

            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date=date,
                time=time,
                reason=reason
            )

            return redirect("appointments")

        except Exception as e:
            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments_list,
                "error": str(e)
            })

    return render(request, "hospital/appointments.html", {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments_list
    })
# =========================
# PRESCRIPTIONS VIEW
# =========================
from django.shortcuts import render, redirect
from .models import Prescription
from doctors.models import Doctor
from patients.models import Patient


def prescriptions(request):
    # Load required data
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    prescriptions = Prescription.objects.select_related(
        "doctor", "patient"
    ).order_by("-created_at")

    # =========================
    # CREATE PRESCRIPTION (POST)
    # =========================
    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")
        medication = request.POST.get("medication")
        dosage = request.POST.get("dosage", "")
        instructions = request.POST.get("instructions", "")

        # Validation
        if not doctor_id or not patient_id or not medication:
            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": "Doctor, patient, and medication are required"
            })

        try:
            Prescription.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                medication=medication,
                dosage=dosage,
                instructions=instructions
            )

            return redirect("prescriptions")

        except Exception as e:
            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": str(e)
            })

    # =========================
    # GET PAGE
    # =========================
    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": prescriptions
    })

# =========================
# REGISTER VIEW
# =========================
def register_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Please fill all fields"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("dashboard")

    return render(request, "hospital/register.html", {"error": error})


# =========================
# DOCTOR LIST VIEW
# =========================
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctor_list.html", {"doctors": doctors})


# =========================
# ADMIT PATIENT
# =========================
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    patient.is_inpatient = True
    patient.admitted_at = timezone.now()
    patient.save()

    return redirect('reception_dashboard')

from django.contrib.auth.models import User
from django.http import HttpResponse

def fix_admin(request):
    User.objects.filter(username="admin").delete()

    User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        password="1234"
    )

    return HttpResponse("Admin reset successful")

from django.http import HttpResponse

def test_view(request):
    return HttpResponse("OK WORKING")