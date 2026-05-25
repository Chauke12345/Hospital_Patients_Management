from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from hospital import views


urlpatterns = [
    # =========================
    # ADMIN
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # AUTH
    # =========================
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # =========================
    # DASHBOARD
    # =========================
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # =========================
    # PATIENTS
    # =========================
    path("reception/", views.reception, name="reception"),
    path("reception/edit/<int:pk>/", views.edit_patient, name="edit_patient"),

    path("patients/", views.patient_list, name="patients_list"),
    path("patients/delete/<int:pk>/", views.delete_patient, name="delete_patient"),
    path("discharge/<int:pk>/", views.discharge_patient, name="discharge_patient"),

    # =========================
    # DOCTORS
    # =========================
    path("", views.dashboard, name="dashboard"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("patients/", views.patient_list, name="patient_list"),
    # =========================
    # APPOINTMENTS
    # =========================
    path("appointments/", views.appointments_list, name="appointments_list"),
    path("appointments/delete/<int:pk>/", views.delete_appointment, name="delete_appointment"),

    # =========================
    # PRESCRIPTIONS
    # =========================
    path("prescriptions/", views.prescription_list, name="prescriptions_list"),
    path("prescriptions/create/", views.create_prescription, name="create_prescription"),
    path("prescriptions/edit/<int:pk>/", views.edit_prescription, name="edit_prescription"),
    path("prescriptions/delete/<int:pk>/", views.delete_prescription, name="delete_prescription"),

    # =========================
    # EMERGENCIES
    # =========================
    path("emergencies/", views.emergency_list, name="emergency_list"),
    path("emergencies/create/", views.create_emergency, name="create_emergency"),
    path("emergencies/edit/<int:id>/", views.edit_emergency, name="edit_emergency"),
    path("emergencies/admit/<int:id>/", views.admit_patient, name="admit_patient"),

   
   
]