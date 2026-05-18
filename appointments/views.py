from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


def appointments(request):
    # Load all required data
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    # Show newest appointments first (better UX)
    appointments_list = Appointment.objects.select_related(
        "doctor", "patient"
    ).order_by("-created_at")

    # =========================
    # CREATE APPOINTMENT (POST)
    # =========================
    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")
        date = request.POST.get("date")
        time = request.POST.get("time")
        reason = request.POST.get("reason", "")

        # Basic validation
        if not doctor_id or not patient_id or not date or not time:
            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments_list,
                "error": "All required fields must be filled"
            })

        try:
            Appointment.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
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
                "error": f"Error creating appointment: {str(e)}"
            })

    # =========================
    # GET REQUEST (PAGE LOAD)
    # =========================
    return render(request, "hospital/appointments.html", {
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