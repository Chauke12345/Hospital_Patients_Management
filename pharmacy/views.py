from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription
from doctors.models import Doctor
from patients.models import Patient


def pharmacy_dashboard(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    prescriptions_list = Prescription.objects.select_related(
        "doctor", "patient"
    ).order_by("-created_at")

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")
        medication = request.POST.get("medication")
        dosage = request.POST.get("dosage", "")
        instructions = request.POST.get("instructions", "")

        if not doctor_id or not patient_id or not medication:
            return render(request, "pharmacy/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions_list,
                "error": "Doctor, patient, and medication are required"
            })

        Prescription.objects.create(
            doctor_id=doctor_id,
            patient_id=patient_id,
            medication=medication,
            dosage=dosage,
            instructions=instructions
        )

        return redirect("pharmacy_dashboard")

    return render(request, "pharmacy/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": prescriptions_list
    })


def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)

    if request.method == "POST":
        prescription.delete()

    return redirect("pharmacy_dashboard")