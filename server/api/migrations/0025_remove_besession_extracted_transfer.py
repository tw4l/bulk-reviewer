# Generated by Django 2.0.6 on 2018-06-28 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20180627_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='besession',
            name='extracted_transfer',
        ),
    ]