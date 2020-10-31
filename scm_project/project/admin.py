from django.contrib import admin
from .models import Project, Problem, Collaborator, Comment
# Register your models here.
admin.site.register(Project)
admin.site.register(Problem)
admin.site.register(Collaborator)
admin.site.register(Comment)

