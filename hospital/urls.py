from django.contrib import admin
from django.urls import path

from hospital import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.dashboard, name="dashboard"),

    path("reception/", views.reception, name="reception"),
    path("reception/edit/<int:pk>/", views.edit_patient, name="edit_patient"),
    path("patients/", views.patient_list, name="patients_list"),
    path("discharge/<int:pk>/", views.discharge_patient, name="discharge_patient"),

    path("doctors/", views.doctor_list, name="doctor_list"),

    path("appointments/", views.appointments_list, name="appointments_list"),
    path("appointments/delete/<int:id>/", views.delete_appointment, name="delete_appointment"),

    path("prescriptions/", views.prescription_list, name="prescriptions_list"),
    path("prescriptions/create/", views.create_prescription, name="create_prescription"),
    path("prescriptions/edit/<int:id>/", views.edit_prescription, name="edit_prescription"),

    path("emergencies/", views.emergency_list, name="emergency_list"),
    path("emergencies/create/", views.create_emergency, name="create_emergency"),
    path("emergencies/edit/<int:id>/", views.edit_emergency, name="edit_emergency"),

    path("emergencies/admit/<int:id>/", views.admit_patient, name="admit_patient"),

    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("prescriptions/delete/<int:pk>/", views.delete_prescription, name="delete_prescription"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/delete/<int:id>/", views.delete_patient, name="delete_patient")
]