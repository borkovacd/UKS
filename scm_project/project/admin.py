from django.contrib import admin
from .models import Project, Problem, Collaborator, Comment, Label
# Register your models here.
admin.site.register(Project)
admin.site.register(Problem)
admin.site.register(Label)
admin.site.register(Collaborator)
admin.site.register(Comment)

