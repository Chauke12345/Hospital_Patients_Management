from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


def appointment_list(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    appointments_list = Appointment.objects.select_related(
        "doctor", "patient"
    ).order_by("-id")

    # =========================
    # CREATE APPOINTMENT (POST)
    # =========================
    if request.method == "POST":
        doctor = get_object_or_404(Doctor, id=request.POST.get("doctor"))
        patient = get_object_or_404(Patient, id=request.POST.get("patient"))

        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            reason=request.POST.get("reason", "")
        )

        return redirect("appointments")

    # =========================
    # GET REQUEST (PAGE LOAD)
    # =========================
    return render(request, "appointments/appointments.html", {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments_list
    })


# =========================
# DELETE APPOINTMENT
# =========================
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        appointment.delete()

    return redirect("appointments")