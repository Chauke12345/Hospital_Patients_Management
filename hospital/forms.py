from django import forms
from .models import Appointment, Ward

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "ward", "date", "time", "reason"]
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["ward"].queryset = Ward.objects.all()
        self.fields["ward"].empty_label = "Select Ward"