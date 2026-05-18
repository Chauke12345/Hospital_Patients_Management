from django.urls import path
from . import views

urlpatterns = [
    path('', views.reception_dashboard, name='reception_dashboard'),
    path('add-patient/', views.add_patient, name='add_patient'),
    
]