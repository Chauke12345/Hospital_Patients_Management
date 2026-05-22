from django.contrib import admin
from django.urls import path

from hospital import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # =========================
    # ADMIN
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # DASHBOARD
    # =========================
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # =========================
    # PATIENTS / RECEPTION
    # =========================
    path("reception/", views.reception, name="reception"),
    path("reception/edit/<int:pk>/", views.edit_patient, name="edit_patient"),
    path("patients/", views.patient_list, name="patients_list"),
    path("discharge/<int:pk>/", views.discharge_patient, name="discharge_patient"),

    # =========================
    # DOCTORS
    # =========================
    path("doctors/", views.doctor_list, name="doctor_list"),

    # =========================
    # APPOINTMENTS
    # =========================
    path("appointments/", views.appointments_list, name="appointments_list"),
    path("appointments/delete/<int:id>/", views.delete_appointment, name="delete_appointment"),

    # =========================
    # PRESCRIPTIONS
    # =========================
    path("prescriptions/", views.prescription_list, name="prescriptions_list"),
    path("prescriptions/create/", views.create_prescription, name="create_prescription"),
    path("prescriptions/edit/<int:id>/", views.edit_prescription, name="edit_prescription"),

    # =========================
    # EMERGENCIES
    # =========================
    path("emergencies/", views.emergency_list, name="emergency_list"),
    path("emergencies/create/", views.create_emergency, name="create_emergency"),
    path("emergencies/edit/<int:id>/", views.edit_emergency, name="edit_emergency"),

    # =========================
    # AUTH
    # =========================
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]