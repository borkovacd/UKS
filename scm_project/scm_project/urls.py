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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users  import views as user_views
from project.views import ( ProjectListView, 
                            ProjectDetailView, 
                            ProjectCreateView, 
                            ProjectUpdateView, 
                            ProjectDeleteView,
                            
                            ProblemCreateView,
                            ProblemDetailView, 
                            ProblemListView,
                            ProblemDeleteView,

                            LabelCreateView,
                            LabelDetailView,
                            LabelListView,
                            LabelUpdateView,
                            LabelDeleteView

                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('projects', ProjectListView.as_view(), name='home'),
    path('', ProjectListView.as_view(), name='home'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

    path('problem/new/', ProblemCreateView.as_view(), name='problem-create'),
    path('problem/<int:pk>/', ProblemDetailView.as_view(), name='problem-detail'),
    path('problems', ProblemListView.as_view(), name='problems'),
    path('problem/<int:pk>/delete/', ProblemDeleteView.as_view(), name='problem-delete'),

    path('labels', LabelListView.as_view(), name='labels'),
    path('label/<int:pk>/', LabelDetailView.as_view(), name='label-detail'),
    path('label/new/', LabelCreateView.as_view(), name='label-create'),
    path('label/<int:pk>/update/', LabelUpdateView.as_view(), name='label-update'),
    path('label/<int:pk>/delete/', LabelDeleteView.as_view(), name='label-delete'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
