# Generated by Django 3.1.2 on 2020-10-26 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0022_auto_20201026_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='closed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='problem',
            name='reported_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='openers', to=settings.AUTH_USER_MODEL),
        ),
    ]