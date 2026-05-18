from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription
from doctors.models import Doctor
from patients.models import Patient


def prescriptions(request):
    # Load required data
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    prescriptions_list = Prescription.objects.select_related(
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
                "prescriptions": prescriptions_list,
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
                "prescriptions": prescriptions_list,
                "error": str(e)
            })

    # =========================
    # GET PAGE
    # =========================
    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": prescriptions_list
    })


# =========================
# DELETE PRESCRIPTION
# =========================
def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    if request.method == "POST":
        prescription.delete()

    return redirect("prescriptions")