from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

user_choices  = [
    ('Core-2nd Year','Core-2nd Year'),
    ('Core-1st Year','Core-1st Year'),
    ('Board', 'Board'),
    ('Judge','Judge'),
    ('Speaker','Speaker'),
    ('Faculty','Faculty'),
    ('Others','Others')
]
track_choices = [
    ('Security','Security'),
    ('Healthcare','Healthcare'),
    ('Fintech','Fintech'),
    ('Developer tools','Developer tools'),
    ('IOT','IOT'),
    ('Sustainability','Sustainability'),
    ('Open Innovation','Open Innovation'),
    ('Blockchain','Blockchain')
]
class UserType(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    type_of_user = models.CharField(default='Core-2nd Year',choices=user_choices,max_length=40)
    
    def __str__(self):
        return '{} - {}'.format(self.user.username,self.type_of_user)

class TeamInfo(models.Model):
    id  = models.UUIDField(default=uuid.uuid4,primary_key=True)
    team_name = models.CharField(max_length=100)
    idea = models.TextField()
    team_leader = models.CharField(max_length=50)
    team_leader_phone = models.CharField(max_length=50)
    team_memeber_1 = models.CharField(max_length=100,blank=True)
    team_memeber_2 = models.CharField(max_length=100,blank=True)
    team_memeber_3 = models.CharField(max_length=100,blank=True)
    team_memeber_4 = models.CharField(max_length=100,blank=True)
    track = models.CharField(max_length=100,choices=track_choices)


    def __str__(self):
        return self.team_name



class evaluator(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    evaluator_object = models.ForeignKey(UserType,on_delete=models.CASCADE)
    team = models.ForeignKey(TeamInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.team.team_name
    


