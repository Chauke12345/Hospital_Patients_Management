from django.urls import path
from . import views

urlpatterns = [
    path("", views.appointment_list, name="appointments"),
    path("add/", views.add_appointment, name="add_appointment"),
    path("delete/<int:id>/", views.delete_appointment, name="delete_appointment"),
]