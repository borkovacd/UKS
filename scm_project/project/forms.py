from django import forms
from .models import (   
                    Project, 
                    Problem,
                    Label, 
                    Milestone
                    )
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus import DatePickerInput
class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date', 'project']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'})
        }
