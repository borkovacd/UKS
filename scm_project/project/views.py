
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import DateInput
from django.urls import reverse
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
                    Milestone,
                    Collaborator
                    )

from .forms import MilestoneForm, AddCollaboratorForm, ProblemForm, LabelForm
from django.contrib.auth.models import User
from django.contrib import messages



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.filter(project_id=self.object)
        context['milestones'] = Milestone.objects.filter(project_id = self.object)
        context['problems'] = Problem.objects.filter(project_id = self.object)
        context['collaborators'] = Collaborator.objects.filter(project_id = self.object)
        return context

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
"""class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem
    fields = ['title', 'description', 'project']

    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        return super().form_valid(form)
"""
def addProblem(request, pk):
    form = ProblemForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_problem = form.save(commit=False)
            new_problem.project_id = pk;
            new_problem.reported_by = request.user
            new_problem.save()
            messages.success(request, f'Successfully added new problem!')
            return redirect(reverse('project-detail', args=[pk]))
    return render(request, 'project/problem_form.html', {'form': form})


# parameters -> request, project_id, problem_id
@login_required
def close_problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    current_user = request.user
    problem.opened = False
    problem.save()
    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))

# parameters -> request, project_id, problem_id
@login_required
def open_problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    current_user = request.user
    problem.opened = True
    problem.save()
    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))

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
"""class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['title', 'color', 'project']
"""
def addLabel(request, pk):
    form = LabelForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_label = form.save(commit=False)
            new_label.project_id = pk;
            new_label.save()
            messages.success(request, f'Successfully added new label!')
            return redirect(reverse('project-detail', args=[pk]))
    return render(request, 'project/label_form.html', {'form': form})


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
    fields = ['title', 'color', 'project']

# MILESTONES
class MilestoneListView(ListView):
    model = Milestone
    template_name = 'project/milestones.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'milestones'
    ordering = ['title']

class MilestoneDetailView(DetailView):
    model = Milestone

"""class MilestoneCreateView(LoginRequiredMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm"""

def addMilestone(request, pk):
    form = MilestoneForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_milestone = form.save(commit=False)
            new_milestone.project_id = pk;
            new_milestone.save()
            messages.success(request, f'Successfully added new milestone!')
            return redirect(reverse('project-detail', args=[pk]))
    return render(request, 'project/milestone_form.html', {'form': form})


class MilestoneUpdateView(LoginRequiredMixin, UpdateView):
    model = Milestone
    form_class = MilestoneForm

class MilestoneDeleteView(LoginRequiredMixin, DeleteView):
    model = Milestone
    success_url = '/milestones'


# COLLABORATORS

# class AddCollaboratorView(LoginRequiredMixin, CreateView):
#     model = Collaborator
#     fields = ['user']

def addCollaborator(request, pk):
    form = AddCollaboratorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_collaborator = form.save(commit=False)
            new_collaborator.project_id = pk;
            new_collaborator.save()
            messages.success(request, f'Successfully added new collaborator!')
            return redirect(reverse('project-detail', args=[pk]))
    return render(request, 'project/collaborator_form.html', {'form': form})

class CollaboratorListView(ListView):
    model = Collaborator
    template_name = 'project/collaborators.html'
    context_object_name = 'collaborators'

class CollaboratorDetailView(DetailView):
    model = Collaborator

class CollaboratorDeleteView(LoginRequiredMixin, DeleteView):
    model = Collaborator
    success_url = '/collaborators'



