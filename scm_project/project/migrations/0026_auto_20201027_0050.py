# Generated by Django 3.1.2 on 2020-10-26 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20201026_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
