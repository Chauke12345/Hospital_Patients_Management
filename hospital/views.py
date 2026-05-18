from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponse

User = get_user_model()

# =========================
# MODELS (CLEAN IMPORTS)
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
def reception(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            age = request.POST.get("age")
            doctor_id = request.POST.get("doctor")

            doctor = get_object_or_404(Doctor, id=doctor_id)

            try:
                age = int(age)
            except (ValueError, TypeError):
                return render(request, "hospital/reception.html", {
                    "doctors": doctors,
                    "error": "Age must be a valid number"
                })

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

        except Exception:
            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Something went wrong while saving patient"
            })

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })


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

    return redirect("reception_dashboard")


# =========================
# ADMIN RESET (DEV ONLY)
# =========================
def fix_admin(request):
    User.objects.filter(username="admin").delete()

    User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        password="1234"
    )

    return HttpResponse("Admin reset successful")


# =========================
# TEST VIEW
# =========================
def test_view(request):
    return HttpResponse("OK WORKING")