# Generated by Django 5.1.2 on 2025-03-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeker', '0010_alter_resume_email_alter_resume_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='job_type',
            field=models.CharField(blank=True, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contractual', 'Contractual'), ('Internship', 'Internship')], max_length=100),
        ),
    ]
