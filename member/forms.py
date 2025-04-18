from django import forms
from Sparky.models import *

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['treatment','dentist','date','time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }

class AppointmentDateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }
