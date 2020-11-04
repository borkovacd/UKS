
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import DateInput
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .filters import ProblemFilter
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

from .forms import MilestoneForm, AddCollaboratorForm, ProblemForm, LabelForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormMixin



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
        context['opened_problems'] = Problem.objects.filter(project_id = self.object, opened = True)
        context['closed_problems'] = Problem.objects.filter(project_id = self.object, opened = False)
        return context


@login_required
def opened_problems(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    problems = Problem.objects.filter(project_id = project.pk, opened = True)

    labels = Label.objects.filter(project_id = project.pk)
    milestones = Milestone.objects.filter(project_id = project.pk)
    collaborators = Collaborator.objects.filter(project_id = project.pk)
    pk = project_id
    context = {
        'project' : project,
        'problems' : problems,
        'labels' : labels,
        'milestones' : milestones,
        'collaborators' : collaborators
    }
    return render(request, 'project/problems.html', context=context)

@login_required
def closed_problems(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    problems = Problem.objects.filter(project_id = project_id, opened = False)

    labels = Label.objects.filter(project_id = project.pk)
    milestones = Milestone.objects.filter(project_id = project.pk)
    collaborators = Collaborator.objects.filter(project_id = project.pk)
    pk = project_id
    context = {
        'project' : project,
        'problems' : problems,
        'labels' : labels,
        'milestones' : milestones,
        'collaborators' : collaborators
    }
    return render(request, 'project/problems.html', context=context)

@login_required
def opened_milestones(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    milestones = Milestone.objects.filter(project_id = project.pk, opened = True)

    labels = Label.objects.filter(project_id = project.pk)
    problems = Milestone.objects.filter(project_id = project.pk)
    collaborators = Collaborator.objects.filter(project_id = project.pk)
    pk = project_id
    context = {
        'project' : project,
        'problems' : problems,
        'labels' : labels,
        'milestones' : milestones,
        'collaborators' : collaborators
    }
    return render(request, 'project/milestones.html', context=context)

@login_required
def closed_milestones(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    milestones = Milestone.objects.filter(project_id = project.pk, opened = False)

    labels = Label.objects.filter(project_id = project.pk)
    problems = Milestone.objects.filter(project_id = project.pk)
    collaborators = Collaborator.objects.filter(project_id = project.pk)
    pk = project_id
    context = {
        'project' : project,
        'problems' : problems,
        'labels' : labels,
        'milestones' : milestones,
        'collaborators' : collaborators
    }
    return render(request, 'project/milestones.html', context=context)


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
    """milestone = Milestone.objects.filter(project_id = pk).values_list('title', 'description')
                form.fields['milestone'].queryset = milestone
            """
    form.fields['milestone'].queryset = Milestone.objects.filter(project_id = pk)
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
    problem.date_closed = timezone.now()
    problem.closed_by = current_user
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

@login_required
def set_milestone_view(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    project_milestones = Milestone.objects.filter(project=problem.project_id)
    return render(request, 'project/link_milestone.html', {'problem': problem, 'milestones': project_milestones})

@login_required
def link_milestone(request, problem_id, milestone_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    problem.milestone = milestone
    problem.save()
    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))

@login_required
def unlink_milestone(request, problem_id, milestone_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    problem.milestone = None
    problem.save()
    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))

@login_required
def set_label_view(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    project_labels = Label.objects.filter(project=problem.project_id)
    differentLabels = []
    existsAlready = False
    for temp_label in project_labels:
        for temp_label2 in problem.labels.all():
            if temp_label.id == temp_label2.id:
                existsAlready = True

        if existsAlready == False:
            differentLabels.append(temp_label)

        existsAlready = False

    return render(request, 'project/apply_label.html', {'problem': problem, 'differentLabels': differentLabels})

@login_required
def apply_label(request, problem_id, label_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    label = get_object_or_404(Label, pk=label_id)
    problem.labels.add(label)
    problem.save()
    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))

@login_required
def assign_user_view(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    project_collaborators = Collaborator.objects.filter(project=problem.project_id)
    project = get_object_or_404(Project, pk=problem.project_id)

    users = User.objects.all()
    for temp_user in users:
        if temp_user.username == project.author.username:
            author = temp_user

    notAssignedUsers = []
    assignedAlready = False
    for temp_collaborator_user in project_collaborators:
        for temp_user in problem.assignees.all():
            if temp_collaborator_user.user.username == temp_user.username:
                assignedAlready = True

        if assignedAlready == False:
            notAssignedUsers.append(temp_collaborator_user.user)

        assignedAlready = False

    assignedAlready = False
    for temp_user in problem.assignees.all():
        if author.username == temp_user.username:
            assignedAlready = True

        if assignedAlready == False:
            notAssignedUsers.append(author)

    assignedAlready = False

    return render(request, 'project/assign_user.html', {'problem': problem, 'users': notAssignedUsers})

@login_required
def assign_user(request, problem_id, username):
    problem = get_object_or_404(Problem, pk=problem_id)
    users = User.objects.all()

    for temp_user in users:
        if temp_user.username == username:
            problem.assignees.add(temp_user)
            problem.save()

    pk = problem_id
    return redirect(reverse('problem-detail', args=[pk]))


class ProblemDetailView(FormMixin, DetailView):
    model = Problem
    context_object_name = 'comment'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('problem-detail', kwargs={'pk': self.object.pk})

    # def get_object(self):
    #     try:
    #         my_object = User.objects.get(id=self.kwargs.get('pk'))
    #         return my_object
    #     except self.model.DoesNotExist:
    #         raise Http404("No MyModel matches the given query.")

    def get_context_data(self, *args, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(*args, **kwargs)
        comment = self.get_object()
        # form
        context['form'] = self.get_form()
        context['comment'] = comment
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        comment = form.save()
        problem = get_object_or_404(Problem, pk=self.object.pk)
        problem.comments.add(comment)
        problem.save()
        return super(ProblemDetailView, self).form_valid(form)


class ProblemListView(ListView):
    model = Problem
    template_name = 'project/problems.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'problems'
    ordering = ['title']

class ProblemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Problem
    success_url = '/'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problems = Problem.objects.filter(project_id = self.object.project_id)
        labelProblems = []
        for problem in problems:
            for label in problem.labels.all():
                if label.id == self.object.id:
                    labelProblems.append(problem)

        context['problems'] = labelProblems
        return context

class LabelListView(ListView):
    model = Label
    template_name = 'project/labels.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'labels'
    ordering = ['title']

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    success_url = '/'


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm

# MILESTONES
class MilestoneListView(ListView):
    model = Milestone
    template_name = 'project/milestones.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'milestones'
    ordering = ['title']

class MilestoneDetailView(DetailView):
    model = Milestone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Problem.objects.filter(milestone_id = self.object)
        return context


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
    success_url = '/'

# parameters -> request, project_id, problem_id
@login_required
def close_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    current_user = request.user
    milestone.opened = False
    milestone.date_closed = timezone.now()
    milestone.save()
    pk = milestone_id
    return redirect(reverse('milestone-detail', args=[pk]))

# parameters -> request, project_id, problem_id
@login_required
def open_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    current_user = request.user
    milestone.opened = True
    milestone.save()
    pk = milestone_id
    return redirect(reverse('milestone-detail', args=[pk]))

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
    success_url = '/'



