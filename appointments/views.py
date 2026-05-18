from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


# =========================
# ADD APPOINTMENT
# =========================
def add_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time")
        reason = request.POST.get("reason")

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            reason=reason
        )

        return redirect("appointments")

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.select_related("patient", "doctor").all()

    return render(request, "appointments.html", {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments
    })


# =========================
# DELETE APPOINTMENT
# =========================
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        appointment.delete()

    return redirect("appointments")