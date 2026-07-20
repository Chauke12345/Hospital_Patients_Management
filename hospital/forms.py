from django import forms
from .models import Appointment, Ward, Patient


# =========================
# PATIENT FORM
# =========================
class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = [
            "name",
            "age",
            "gender",
            "phone",
            "ward",
            "reason",
            "priority",
            "doctor",
            "is_inpatient",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

        self.fields["ward"].queryset = Ward.objects.all()
        self.fields["ward"].empty_label = "Select Ward"


# =========================
# APPOINTMENT FORM
# =========================
class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            "patient",
            "doctor",
            "date",
            "time",
            "reason"
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })