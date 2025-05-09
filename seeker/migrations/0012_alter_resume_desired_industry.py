# Generated by Django 5.1.2 on 2025-03-21 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0012_alter_blogpost_image'),
        ('seeker', '0011_alter_resume_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='desired_industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to='jobboard.jobcategory'),
        ),
    ]
