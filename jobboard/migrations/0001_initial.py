# Generated by Django 5.1.2 on 2025-02-13 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_employerprofile_logo_seekerprofile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company_industry_type', models.CharField(max_length=255)),
                ('no_of_vacancy', models.PositiveIntegerField()),
                ('application_deadline', models.DateField()),
                ('age_range', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50)),
                ('contact_person', models.CharField(max_length=255)),
                ('experience_required', models.CharField(max_length=150)),
                ('cv_receive_method', models.CharField(choices=[('Online CV/Resume', 'Online CV/Resume'), ('Email Attachment', 'Email Attachment'), ('Walk-in Interview', 'Walk-in Interview'), ('Hard Copy CV', 'Hard Copy CV')], max_length=255)),
                ('job_type', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Contractual', 'Contractual'), ('Internship', 'Internship')], max_length=50)),
                ('job_level', models.CharField(choices=[('Entry Level', 'Entry Level'), ('Mid Level', 'Mid Level'), ('Top Level', 'Top Level')], max_length=50)),
                ('applicant_photo_required', models.BooleanField(default=False)),
                ('educational_qualification', models.TextField()),
                ('job_description', models.TextField()),
                ('job_responsibilities', models.TextField()),
                ('job_requirements', models.TextField()),
                ('other_benefits', models.TextField(blank=True, null=True)),
                ('job_location', models.CharField(max_length=200)),
                ('exclusive_job', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to='accounts.employerprofile')),
                ('job_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_posts_category', to='jobboard.jobcategory')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(blank=True, upload_to='media/resumes/', verbose_name='Resume')),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.seekerprofile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobboard.jobpost')),
            ],
        ),
    ]
