from django.urls import path
from . import views
from .views import fix_admin

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('reception/', views.reception, name='reception'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('patients/', views.patient_list, name='patients'),

    path('fix-admin/', fix_admin),
]