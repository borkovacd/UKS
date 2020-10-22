from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from enum import Enum
from colorfield.fields import ColorField
from colorful.fields import RGBColorField
from functools import partial
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
#DateInput = partial(models.DateInput, {'class': 'datepicker'})
from django import forms

class Problem_State(Enum):
    OPEN = 1
    CLOSED = 2

class Project(models.Model):
    title = models.CharField(max_length=100)
    git_repository = models.CharField(max_length=100)
    date_created = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    collaborators = models.ManyToManyField(User, related_name='collaborations')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(default = timezone.now, null=True)
    # rekurzija
    base_problem = models.ForeignKey('self', related_name='problem', on_delete=models.CASCADE, null=True, blank=True)
    #linked_milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)
    #current_assignee = models.ForeignKey(User, related_name='assigned', on_delete=models.SET_NULL, null=True)
	# problem state

    def get_absolute_url(self):
        return reverse('problem-detail', kwargs={'pk': self.pk})


class Label(models.Model):
    title = models.CharField(max_length=100)
    #color = ColorField(default='#FF0000')
    color = RGBColorField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    problems = models.ManyToManyField(Problem, related_name='labels')

    def get_absolute_url(self):
        return reverse('label-detail', kwargs={'pk': self.pk})


class Milestone(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    due_date = models.DateField(default = timezone.now)
    date_created = models.DateTimeField(default = timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)  

    def get_absolute_url(self):
        return reverse('milestone-detail', kwargs={'pk': self.pk})      
