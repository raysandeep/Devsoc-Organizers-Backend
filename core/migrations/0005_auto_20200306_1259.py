# Generated by Django 3.0.4 on 2020-03-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200306_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminfo',
            name='track',
            field=models.CharField(choices=[('Security', 'Security'), ('Healthcare', 'Healthcare'), ('Fintech', 'Fintech'), ('Developer tools', 'Developer tools'), ('Internet of Things', 'Internet of Things'), ('Sustainability', 'Sustainability'), ('Open Innovation', 'Open Innovation'), ('Blockchain', 'Blockchain')], max_length=100),
        ),
    ]