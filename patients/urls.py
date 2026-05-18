from django.urls import path
from .views import patient_list, add_patient, discharge_patient

urlpatterns = [
    path("", patient_list, name="patient_list"),
    path("add/", add_patient, name="add_patient"),
    path("discharge/<int:patient_id>/", discharge_patient, name="discharge_patient"),
]