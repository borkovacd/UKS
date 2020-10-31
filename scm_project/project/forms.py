from django import forms
from .models import (
                    Project,
                    Problem,
                    Label,
                    Milestone,
                    Collaborator,
                    Comment
                    )
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus import DatePickerInput

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'})
        }

class AddCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ['user']

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'milestone']

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['title', 'description', 'color']

class CommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ['text']
