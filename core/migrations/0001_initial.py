# Generated by Django 3.0.4 on 2020-03-06 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=100)),
                ('idea', models.TextField()),
                ('team_leader', models.CharField(max_length=50)),
                ('team_leader_phone', models.CharField(max_length=50)),
                ('team_memeber_1', models.CharField(blank=True, max_length=100)),
                ('team_memeber_2', models.CharField(blank=True, max_length=100)),
                ('team_memeber_3', models.CharField(blank=True, max_length=100)),
                ('team_memeber_4', models.CharField(blank=True, max_length=100)),
                ('track', models.CharField(choices=[('Security', 'Security'), ('Healthcare', 'Healthcare'), ('Fintech', 'Fintech'), ('Developer tools', 'Developer tools'), ('IOT', 'IOT'), ('Sustainability', 'Sustainability'), ('Open Innovation', 'Open Innovation'), ('Blockchain', 'Blockchain')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_user', models.CharField(choices=[('Core-2nd Year', 'Core-2nd Year'), ('Core-1st Year', 'Core-1st Year'), ('Board', 'Board'), ('Judge', 'Judge'), ('Speaker', 'Speaker'), ('Faculty', 'Faculty'), ('Others', 'Others')], default='Core-2nd Year', max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='evaluator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('evaluator_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserType')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TeamInfo')),
            ],
        ),
    ]