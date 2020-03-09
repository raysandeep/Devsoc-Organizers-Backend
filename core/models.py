from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

user_choices  = [
    ('Core-2nd Year','Core-2nd Year'),
    ('Core-1st Year','Core-1st Year'),
    ('Board', 'Board'),
    ('Judge','Judge'),
]
track_choices = [
    ('Security','Security'),
    ('Healthcare','Healthcare'),
    ('Fintech','Fintech'),
    ('Developer tools','Developer tools'),
    ('Internet of Things','Internet of Things'),
    ('Sustainability','Sustainability'),
    ('Open Innovation','Open Innovation'),
    ('Blockchain','Blockchain')
]



class UserType(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=100,choices=user_choices)
    
    def __str__(self):
        return '{} - {}'.format(self.user.username,self.category)



class TeamInfo(models.Model):
    id  = models.UUIDField(default=uuid.uuid4,primary_key=True)
    team_name = models.CharField(max_length=100)
    idea = models.TextField()
    team_number = models.IntegerField()
    team_leader = models.CharField(max_length=50)
    team_leader_phone = models.CharField(max_length=50)
    team_memeber_1 = models.CharField(max_length=100,blank=True)
    team_memeber_2 = models.CharField(max_length=100,blank=True)
    team_memeber_3 = models.CharField(max_length=100,blank=True)
    team_memeber_4 = models.CharField(max_length=100,blank=True)
    track = models.CharField(max_length=100,choices=track_choices)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.team_name



class evaluator(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    round_level = models.IntegerField()
    evaluator_object = models.ForeignKey(UserType,on_delete=models.CASCADE)
    team = models.ForeignKey(TeamInfo,on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - Round - {}'.format(self.team.team_name,self.evaluator_object.user.username,self.round_level)
    

class Messaging(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    team = models.ForeignKey(TeamInfo,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message_conf = models.BooleanField(default=False)#false for general and true for evaluation
    message_heading = models.CharField(max_length=100)
    message_body = models.CharField(max_length=500)
    def __str__(self):
        return self.message_heading


    
class Notifications(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username
     

class EvaluationParms(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    evaluator = models.OneToOneField(evaluator,on_delete=models.CASCADE)
    novelty_slider = models.IntegerField()
    tech_feasability_slider = models.IntegerField()
    work_done_slider = models.IntegerField(default=0)
    impact_slider = models.IntegerField()
    presentation_quality_slider = models.IntegerField()
    bussiness_model_slider = models.IntegerField()
    scalability_slider = models.IntegerField()
    remarks = models.CharField(max_length=300)
    notes = models.CharField(max_length=300,default='Not Filled')
    suggesstions_given = models.CharField(max_length=300,default='Not Filled')

    def __str__(self):
        return '{} - Evaluated by {} for round {} '.format(self.evaluator.team.team_name,self.evaluator.evaluator_object.user.username,self.evaluator.round_level)
    
