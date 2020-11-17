from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Project

# @receiver(post_save, sender=Collaborator)
# def update_collaborator(sender, instance, created, **kwargs):
#     if created:
#         Collaborator.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
