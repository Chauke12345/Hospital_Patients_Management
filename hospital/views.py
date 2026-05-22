from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

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
    patients = Patient.objects.all()

    context = {
        "patients": patients,
        "total_patients": patients.count(),
        "admitted": Patient.objects.filter(is_inpatient=True).count(),
        "discharged": Patient.objects.filter(is_discharged=True).count(),
    }
    return render(request, "hospital/dashboard.html", context)


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
        patient = get_object_or_404(Patient, pk=patient_id) if patient_id else Patient(is_inpatient=True)

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
# APPOINTMENTS
# =========================
def appointments_list(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        if not patient_id or not doctor_id:
            return render(request, "hospital/appointments.html", {
                "patients": patients,
                "doctors": doctors,
                "appointments": appointments,
                "error": "Select both patient and doctor"
            })

        Appointment.objects.create(
            patient=get_object_or_404(Patient, pk=patient_id),
            doctor=get_object_or_404(Doctor, pk=doctor_id),
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
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        if not patient_id or not doctor_id:
            return render(request, "hospital/create_prescription.html", {
                "patients": patients,
                "doctors": doctors,
                "error": "Select both patient and doctor"
            })

        Prescription.objects.create(
            patient=get_object_or_404(Patient, pk=patient_id),
            doctor=get_object_or_404(Doctor, pk=doctor_id),
            medicine_name=request.POST.get("medicine_name"),
            dosage=request.POST.get("dosage"),
            instructions=request.POST.get("instructions"),
        )

        return redirect("prescription_list")

    return render(request, "hospital/create_prescription.html", {
        "patients": patients,
        "doctors": doctors
    })


def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by("-id")
    return render(request, "hospital/prescription_list.html", {"prescriptions": prescriptions})


def edit_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    if request.method == "POST":
        prescription.medicine_name = request.POST.get("medicine_name")
        prescription.dosage = request.POST.get("dosage")
        prescription.instructions = request.POST.get("instructions")
        prescription.save()
        return redirect("prescription_list")

    return render(request, "hospital/edit_prescription.html", {
        "prescription": prescription
    })


# =========================
# EMERGENCY
# =========================
def emergency_list(request):
    emergencies = Emergency.objects.all().order_by("-created_at")
    return render(request, "hospital/emergency_list.html", {"emergencies": emergencies})


def create_emergency(request):
    patients = Patient.objects.all()

    if request.method == "POST":
        Emergency.objects.create(
            patient_id=request.POST["patient"],
            emergency_type=request.POST["emergency_type"],
            severity=request.POST["severity"],
            description=request.POST["description"],
        )
        return redirect("emergency_list")

    return render(request, "hospital/create_emergency.html", {"patients": patients})


def edit_emergency(request, id):
    emergency = get_object_or_404(Emergency, id=id)

    if request.method == "POST":
        emergency.emergency_type = request.POST.get("emergency_type")
        emergency.severity = request.POST.get("severity")
        emergency.description = request.POST.get("description")
        emergency.status = request.POST.get("status")
        emergency.save()
        return redirect("emergency_list")

    return render(request, "hospital/edit_emergency.html", {"emergency": emergency})


# =========================
# ADMISSION
# =========================
def admit_patient(request, emergency_id):
    emergency = get_object_or_404(Emergency, id=emergency_id)

    if request.method == "POST":
        ward_id = request.POST.get("ward")

        Admission.objects.create(
            patient=emergency.patient,
            emergency=emergency,
            ward_id=ward_id,
            admitted_at=timezone.now(),
            status="Active",
        )

        emergency.status = "Admitted"
        emergency.save()

        return redirect("emergency_list")

    return render(request, "hospital/admit_patient.html", {
        "emergency": emergency,
        "wards": Ward.objects.all()
    })


# =========================
# AUTH
# =========================
def signup(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")