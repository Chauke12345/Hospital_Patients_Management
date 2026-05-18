from django.urls import path
from . import views

urlpatterns = [

    # Main appointments page
    path('', views.appointments, name='appointments'),

    # Add appointment (if separate view is needed)
    path('add/', views.add_appointment, name='add_appointment'),

    # Delete appointment
    path('delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
]