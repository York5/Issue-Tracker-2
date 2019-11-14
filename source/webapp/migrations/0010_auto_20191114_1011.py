# Generated by Django 2.2 on 2019-11-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20191107_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='date_finished',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time Finished'),
        ),
        migrations.AlterField(
            model_name='team',
            name='date_started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time Started'),
        ),
    ]