from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import DateInput
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.forms.widgets import HiddenInput
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import (   
                    Project, 
                    Problem,
                    Label, 
                    Milestone
                    )

from .forms import MilestoneForm
class DateInput(forms.DateInput):
    input_type = 'date'

def home(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'project/home.html', context)

# PROJECTS
class ProjectListView(ListView):
    model = Project
    template_name = 'project/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    ordering = ['title']

class ProjectDetailView(DetailView):
    model = Project  

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'git_repository']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 



class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'git_repository']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False 


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False                


# PROBLEMS 
class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        return super().form_valid(form) 


class ProblemDetailView(DetailView):
    model = Problem        

class ProblemListView(ListView):
    model = Problem
    template_name = 'project/problems.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'problems'
    ordering = ['title']

class ProblemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Problem
    success_url = '/problems'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.reported_by:
            return True
        return False                


# LABELS
class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['title', 'color']


class LabelDetailView(DetailView):
    model = Label        

class LabelListView(ListView):
    model = Label
    template_name = 'project/labels.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'labels'
    ordering = ['title']

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    success_url = '/labels'


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['title', 'color']

# MILESTONES    
class MilestoneListView(ListView):
    model = Milestone
    template_name = 'project/milestones.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'milestones'
    ordering = ['title']

class MilestoneDetailView(DetailView):
    model = Milestone  

class MilestoneCreateView(LoginRequiredMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm

class MilestoneUpdateView(LoginRequiredMixin, UpdateView):
    model = Milestone
    form_class = MilestoneForm

class MilestoneDeleteView(LoginRequiredMixin, DeleteView):
    model = Milestone
    success_url = '/milestones'             

              