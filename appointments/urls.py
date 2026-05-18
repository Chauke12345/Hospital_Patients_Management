from django.urls import path
from . import views

urlpatterns = [
    # Main appointments page
    path("", views.appointment_list, name="appointments"),

    # Add appointment (only if you really use it)
    path("add/", views.add_appointment, name="add_appointment"),

    # Delete appointment
    path("delete/<int:id>/", views.delete_appointment, name="delete_appointment"),
]