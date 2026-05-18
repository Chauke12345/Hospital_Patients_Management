from django.urls import path
from . import views
from .views import fix_admin

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('reception/', views.reception, name='reception'),
    path('appointments/', views.appointments, name='appointments'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('patients/', views.patient_list, name='patients'),

    path('fix-admin/', fix_admin),
]