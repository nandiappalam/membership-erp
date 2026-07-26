from django import forms
from .models import *


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "organisation",
            "assessment_year",
            "event_name",
            "event_date",
            "start_time",
            "end_time",
            "venue",
            "description",
            "registration_open",
            "status",
        ]

        widgets = {

            "organisation": forms.Select(
                attrs={"class": "form-select"}
            ),

            "assessment_year": forms.Select(
                attrs={"class": "form-select"}
            ),

            "event_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Event Name"
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time"
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time"
                }
            ),

            "venue": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Venue"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Description"
                }
            ),

            "registration_open": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }


