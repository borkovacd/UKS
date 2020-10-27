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
from users.models import Profile
from datetime import datetime


class Problem_State(Enum):
    OPEN = 1
    CLOSED = 2

class Project(models.Model):
    title = models.CharField(max_length=100)
    git_repository = models.CharField(max_length=100)
    date_created = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    #collaborators = models.ManyToManyField(User, related_name='collaborators')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null = True, blank = True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='openers')
    closed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='closers')
    created_time = models.DateTimeField(default = timezone.now, null=True)
    date_closed = models.DateTimeField(null = True)

    base_problem = models.ForeignKey('self', related_name='problem', on_delete=models.CASCADE, null=True, blank=True)
    opened = models.BooleanField(default = True, null = True)

    def get_absolute_url(self):
        return reverse('problem-detail', kwargs={'pk': self.pk}) 

class Label(models.Model):
    title = models.CharField(max_length=100)
    color = RGBColorField()
    description = models.CharField(max_length=100, null = True, blank = True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    problems = models.ManyToManyField(Problem, related_name='labels')

    def get_absolute_url(self):
        return reverse('label-detail', kwargs={'pk': self.pk})


class Milestone(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    due_date = models.DateField(default = timezone.now, null = True, blank = True)
    date_created = models.DateTimeField(default = timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    opened = models.BooleanField(default = True, null = True)
    date_closed = models.DateTimeField(null = True)

    def get_absolute_url(self):
        return reverse('milestone-detail', kwargs={'pk': self.pk})

class Collaborator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null = True)

    def get_absolute_url(self):
        return reverse('collaborator-detail', kwargs={'pk': self.pk})


class Custom_Event(models.Model):
    created_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

class Change_State(Custom_Event):
    current_state = models.CharField(
      max_length=2,
      choices=[(tag, tag.value) for tag in Problem_State]
    )

    @classmethod
    def create(cls, creator, state, problem):
        created_time = datetime.now()
        new_state = cls(creator=creator, problem=problem, current_state=state, created_time=created_time)
        new_state.save()
        return new_state
