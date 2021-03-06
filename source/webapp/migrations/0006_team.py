# Generated by Django 2.2 on 2019-11-06 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0005_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Team Name')),
                ('date_started', models.DateTimeField(auto_now_add=True, verbose_name='Time Started')),
                ('date_finished', models.DateTimeField(auto_now=True, verbose_name='Time Finished')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='project_user', to='webapp.Project', verbose_name='Project')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_project', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
