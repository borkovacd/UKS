"""scm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from project.views import *
from users  import views as user_views
from project.views import ( ProjectListView,
                            ProjectDetailView,
                            ProjectCreateView,
                            ProjectUpdateView,
                            ProjectDeleteView,

                            ProblemDetailView,
                            ProblemListView,
                            ProblemDeleteView,

                            LabelDetailView,
                            LabelListView,
                            LabelUpdateView,
                            LabelDeleteView,

                            MilestoneListView,
                            MilestoneDetailView,
                            MilestoneUpdateView,
                            MilestoneDeleteView,

                            CollaboratorListView,
                            CollaboratorDetailView,
                            CollaboratorDeleteView
                            )
from project import views as project_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('projects', ProjectListView.as_view(), name='home'),
    path('list_projects', home, name='list_projects'),
    path('', ProjectListView.as_view(), name='home'),
    path('collaborations/', collaborations, name='collaborations'),    
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<int:project_id>/problems-opened/', opened_problems, name='opened_problems'),
    path('project/<int:project_id>/problems-closed/', closed_problems, name='closed_problems'),
    path('project/<int:project_id>/milestones-opened/', opened_milestones, name='opened_milestones'),
    path('project/<int:project_id>/milestones-closed/', closed_milestones, name='closed_milestones'),

    path('project/<int:pk>/new-problem/', project_views.addProblem, name='problem-create'),
    path('problem/<int:pk>/', ProblemDetailView.as_view(), name='problem-detail'),
    path('problems', ProblemListView.as_view(), name='problems'),
    path('problem/<int:pk>/delete/', ProblemDeleteView.as_view(), name='problem-delete'),
    path('problem/<int:pk>/update/', ProblemUpdateView.as_view(), name='problem-update'),
    path('problem/<int:problem_id>/close/', close_problem, name='close_problem'),
    path('problem/<int:problem_id>/open/', open_problem, name='open_problem'),
    path('problem/<int:problem_id>/set_milestone/', set_milestone_view, name='set_milestone_view'),
    path('problem/<int:problem_id>/set_milestone/<int:milestone_id>/link/', link_milestone, name='link_milestone'),
    path('problem/<int:problem_id>/set_milestone/<int:milestone_id>/unlink/', unlink_milestone, name='unlink_milestone'),
    path('problem/<int:problem_id>/apply_label/', set_label_view, name='set_label_view'),
    path('problem/<int:problem_id>/apply_label/<int:label_id>/apply/', apply_label, name='apply_label'),
    path('problem/<int:problem_id>/apply_label/<int:label_id>/remove/', remove_label, name='remove_label'),
    path('problem/<int:problem_id>/assign_user/', assign_user_view, name='assign_user_view'),
    path('problem/<int:problem_id>/assign_user/<str:username>/assign/', assign_user, name='assign_user'),
    path('problem/<int:problem_id>/assign_user/<str:username>/remove/', remove_user, name='remove_user'),
    path('problem/<int:problem_id>/update_comment/<int:comment_id>/', update_comment, name='update_comment'),
    path('problem/<int:problem_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('labels', LabelListView.as_view(), name='labels'),
    path('label/<int:pk>/', LabelDetailView.as_view(), name='label-detail'),
    path('project/<int:pk>/new-label/', project_views.addLabel, name='label-create'),
    path('label/<int:pk>/update/', LabelUpdateView.as_view(), name='label-update'),
    path('label/<int:pk>/delete/', LabelDeleteView.as_view(), name='label-delete'),

    path('milestones', MilestoneListView.as_view(), name='milestones'),
    path('milestone/<int:pk>/', MilestoneDetailView.as_view(), name='milestone-detail'),
    path('project/<int:pk>/new-milestone/', project_views.addMilestone, name='milestone-create'),
    path('milestone/<int:pk>/update/', MilestoneUpdateView.as_view(), name='milestone-update'),
    path('milestone/<int:pk>/delete/', MilestoneDeleteView.as_view(), name='milestone-delete'),
    path('milestone/<int:milestone_id>/close/', close_milestone, name='close_milestone'),
    path('milestone/<int:milestone_id>/open/', open_milestone, name='open_milestone'),

    path('collaborators', CollaboratorListView.as_view(), name='collaborators'),
    path('project/<int:pk>/collaborate/', project_views.addCollaborator, name='project-collaborate'),
    path('collaborator/<int:pk>/', CollaboratorDetailView.as_view(), name='collaborator-detail'),
    path('collaborator/<int:pk>/delete/', CollaboratorDeleteView.as_view(), name='collaborator-delete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
