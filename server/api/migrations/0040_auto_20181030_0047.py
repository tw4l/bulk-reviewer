# Generated by Django 2.0.9 on 2018-10-30 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20180728_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='offset',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
