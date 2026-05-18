from django import forms
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['patient'].queryset = Patient.objects.all()