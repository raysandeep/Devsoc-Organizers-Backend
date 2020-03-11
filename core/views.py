from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from pyfcm import FCMNotification

from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
User = get_user_model()
from rest_framework.views import APIView

ROUND_LEVEL = 1

BOARD_METRIX =  0.8
JUDGE_METRIX = 1
CORE_METRIX = 0.7

from .models import (
    evaluator,
    TeamInfo,
    UserType,
    Messaging,
    Notifications,
    EvaluationParms
)

from .serializers import(
    EvaluatorSerializer,
    MessagingSerializer,
    Messaging1Serializer,

    NotificationSerilizer,
    EvaluationParamsSerializer,
    TeamNamesSerializer,
    TeamInfoSerializer,
    EvalFinalSerializer,
    UserTypeSerializer
)

class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        try: 
            data = {
                'token':token_serializer_class(token).data,
                'user_type' : UserType.objects.filter(user=serializer.user)[0].category,
                'username': serializer.user.username,
                'name': serializer.user.first_name+' '+serializer.user.last_name
            }
        
        except:
            return HttpResponse(status=404)
        return Response(
            data=data, status=status.HTTP_200_OK
        )



class EvaluatorList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        list_of_teams=[]
        completed_list = []
        final_data_completed=[]
        not_completed_list=[]
        try:
            list_of_teams = evaluator.objects.filter(evaluator_object__user=request.user).filter(round_level=ROUND_LEVEL)
            completed_list = EvaluationParms.objects.filter(evaluator__round_level=1).filter(evaluator__evaluator_object__user=request.user)
        except evaluator.DoesNotExist:
            return HttpResponse(status=404)
        serializer = EvaluatorSerializer(list_of_teams, many=True)
        serializer1 = EvaluationParamsSerializer(completed_list, many=True)
        
        for i in serializer1.data:
            team_details = {
                'eval_id':i['evaluator']['id'],
                'team_id':i['evaluator']['team']['id'],
                'team_name':i['evaluator']['team']['team_name'],
                'team_number':i['evaluator']['team']['team_number'],
                'team_track':i['evaluator']['team']['track'],

            }
            final_data_completed.append(team_details)
        
        for i in serializer.data:
            team_details = {
                'eval_id':i['id'],
                'team_id':i['team']['id'],
                'team_name':i['team']['team_name'],
                'team_number':i['team']['team_number'],
                'team_track':i['team']['track'],

            }
            if team_details in final_data_completed:
                pass
            else:
                not_completed_list.append(team_details)
        data = {
            'round':ROUND_LEVEL,
            'data':not_completed_list,
            'completed_data':final_data_completed
        }
        return Response(data)

    
class Message(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if not request.data._mutable:
            request.data._mutable = True
            request.data['user']=User.objects.filter(id=request.user.id)[0].id
            request.data['team']=TeamInfo.objects.filter(team_number=request.data['team'])[0].id
            request.data._mutable = False
            serializer = MessagingSerializer(data=request.data)
            print(request.data)
            push_service = FCMNotification(api_key="AIzaSyD8v3e4a3v-rcasU3Mh0KKkPaflm1dW1J4")
            if serializer.is_valid():
                print(serializer.validated_data)
                serializer.save(user=request.user)
                if not serializer.data['message_conf']:
                    devices = Notifications.objects.all()#.exclude(user=request.user) UNCOMMMENT THIS IN FUTURE
                    registration_ids=[]
                    for i in devices:
                        registration_ids.append(i.device_id)
                    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=serializer.data['message_heading'], message_body=serializer.data['message_body'])
                    print(result)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            request.data['user']=request.user
            serializer = MessagingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if Notifications.objects.filter(user=request.user).exists():
            Notifications.objects.filter(user=request.user).update(device_id=request.data['device_id'])
            return HttpResponse(status=200)
        else:
            serializer=NotificationSerilizer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)



class EvaluateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        evaluator1 = evaluator.objects.filter(id=request.data['evaluator']).filter(evaluator_object__user__id=request.user.id).filter(round_level=ROUND_LEVEL)[0]
        print(evaluator)
        serializer=EvaluationParamsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(evaluator=evaluator1)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    def get(self,request):
        try:
            evaluator1 = evaluator.objects.filter(id=request.data['eval_id']).filter(evaluator_object__user__id=request.user.id).filter(round_level=ROUND_LEVEL)[0]
            evalparams = EvaluationParms.objects.filter(evaluator=evaluator1)
        except evaluator.DoesNotExist:
            return HttpResponse(status=404)
        serializer = EvaluationParamsSerializer(evalparams, many=True)
        return Response(serializer.data,status=200)



class GetTeamNames(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        teams = TeamInfo.objects.all()
        serializer = TeamNamesSerializer(teams,many=True)
        return Response(serializer.data,status=200)




class GetTeamInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        metrix=0
        round1={}
        round2={}
        round3={}
        round1_list=[]
        round2_list=[]
        round3_list=[]
        mem_list=[]

        final_score = {
            'round1':0,
            'round2':0,
            'round3':0
        }
        team = TeamInfo.objects.filter(id=id)
        print(team)
        round1_eval = EvaluationParms.objects.filter(evaluator__team=team[0]).filter(evaluator__round_level=1)
        round2_eval = EvaluationParms.objects.filter(evaluator__team=team[0]).filter(evaluator__round_level=2)
        round3_eval = EvaluationParms.objects.filter(evaluator__team=team[0]).filter(evaluator__round_level=3)
        messages_serializer = Messaging.objects.filter(team__id=id)
        teaminfo = TeamInfoSerializer(team, many=True)
        round1 = EvalFinalSerializer(round1_eval,many=True).data
        round2 = EvalFinalSerializer(round2_eval,many=True).data
        round3 = EvalFinalSerializer(round3_eval,many=True).data
        messages = Messaging1Serializer(messages_serializer,many=True)


        team_status=''
        for abc in teaminfo.data:
            if abc['team_memeber_1'] != '':
                mem_list.append(abc['team_memeber_1'])
            if abc['team_memeber_2'] != '':
                mem_list.append(abc['team_memeber_2'])
            if abc['team_memeber_3'] != '':
                mem_list.append(abc['team_memeber_3'])
            if abc['team_memeber_4'] != '':
                mem_list.append(abc['team_memeber_4'])
            if abc['status']==True:
                team_status='Qualified'
            else:
                team_status='Disqualified'
            team_details = {
                'id':abc['id'],
                'team_name':abc['team_name'],
                'idea':abc['idea'],
                'team_number':abc['team_number'],
                'team_leader':abc['team_leader'],
                'team_leader_phone':abc['team_leader_phone'],
                'team_mem':mem_list,
                'track':abc['track'],
                'status':team_status
            }
            break






        if round1_eval.count() != 0:
            for i in round1:
                
                if i['evaluator']['evaluator_object']['category'] == 'Core-2nd Year':
                    metrix=CORE_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Board':
                    metrix=BOARD_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Judge':
                    metrix=JUDGE_METRIX
                score = (i['novelty_slider']+i['tech_feasability_slider']+i['impact_slider']+\
                    i['presentation_quality_slider']+i['bussiness_model_slider']+\
                        i['scalability_slider'])*metrix/6
                eval_data = {
                    'novelty_slider':i['novelty_slider'],
                    'tech_feasability_slider':i['tech_feasability_slider'],
                    'impact_slider':i['impact_slider'],
                    'presentation_quality_slider':i['presentation_quality_slider'],
                    'bussiness_model_slider':i['bussiness_model_slider'],
                    'scalability_slider':i['scalability_slider'],
                    'remarks':i['remarks'],
                    'notes':i['notes'],
                    'suggesstions_given':i['suggesstions_given'],
                    'evalName':i['evaluator']['evaluator_object']['user']['first_name']+' '+i['evaluator']['evaluator_object']['user']['last_name'],
                    'UserId':i['evaluator']['evaluator_object']['user']['id'],
                    'userType':i['evaluator']['evaluator_object']['category'],
                    'score':score
                }
                final_score['round1']+=score
                round1_list.append(eval_data)
                final_score['round1'] = final_score['round1']/round1_eval.count()
        
        if round2_eval.count() != 0:
            for i in round2:
                
                if i['evaluator']['evaluator_object']['category'] == 'Core-2nd Year':
                    metrix=CORE_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Board':
                    metrix=BOARD_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Judge':
                    metrix=JUDGE_METRIX
                score = (i['novelty_slider']+i['tech_feasability_slider']+i['impact_slider']+\
                    i['presentation_quality_slider']+i['bussiness_model_slider']+\
                        i['scalability_slider'])*metrix/6
                eval_data = {
                    'novelty_slider':i['novelty_slider'],
                    'tech_feasability_slider':i['tech_feasability_slider'],
                    'impact_slider':i['impact_slider'],
                    'presentation_quality_slider':i['presentation_quality_slider'],
                    'bussiness_model_slider':i['bussiness_model_slider'],
                    'scalability_slider':i['scalability_slider'],
                    'remarks':i['remarks'],
                    'notes':i['notes'],
                    'suggesstions_given':i['suggesstions_given'],
                    'evalName':i['evaluator']['evaluator_object']['user']['first_name']+' '+i['evaluator']['evaluator_object']['user']['last_name'],
                    'UserId':i['evaluator']['evaluator_object']['user']['id'],
                    'userType':i['evaluator']['evaluator_object']['category'],
                    'score':score
                }
                final_score['round2']+=score
                round2_list.append(eval_data)
                final_score['round2']=final_score['round2']/round2_eval.count()

        if round3_eval.count() != 0:
            for i in round3:
                
                if i['evaluator']['evaluator_object']['category'] == 'Core-2nd Year':
                    metrix=CORE_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Board':
                    metrix=BOARD_METRIX
                elif i['evaluator']['evaluator_object']['category'] == 'Judge':
                    metrix=JUDGE_METRIX
                score = (i['novelty_slider']+i['tech_feasability_slider']+i['impact_slider']+\
                    i['presentation_quality_slider']+i['bussiness_model_slider']+\
                        i['work_done_slider']+i['scalability_slider'])*metrix/7
                eval_data = {
                    'novelty_slider':i['novelty_slider'],
                    'tech_feasability_slider':i['tech_feasability_slider'],
                    'impact_slider':i['impact_slider'],
                    'presentation_quality_slider':i['presentation_quality_slider'],
                    'bussiness_model_slider':i['bussiness_model_slider'],
                    'scalability_slider':i['scalability_slider'],
                    'remarks':i['remarks'],
                    'notes':i['notes'],
                    'work_done_slider':i['work_done_slider'],
                    'evalName':i['evaluator']['evaluator_object']['user']['first_name']+' '+i['evaluator']['evaluator_object']['user']['last_name'],
                    'UserId':i['evaluator']['evaluator_object']['user']['id'],
                    'userType':i['evaluator']['evaluator_object']['category'],
                    'score':score
                }
                final_score['round3']+=score
                round2_list.append(eval_data)
                final_score['round3']=final_score['round3']/round3_eval.count()

        data = {
            'teamInfo':team_details,
            'round1Eval':{
                'FinalScore':final_score['round1'],
                'data':round1_list
            },
            'round2Eval':{
                'FinalScore':final_score['round2'],
                'data':round2_list
            },
            'round3Eval':{
                'FinalScore':final_score['round3'],
                'data':round3_list
            },
            'finalScore':(final_score['round1']+final_score['round2']+final_score['round3'])/3,
            'messages':messages.data
            
        }
        return Response(data,status=200)


class GetTeamInfoSecond(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        mem_list=[]
        team = TeamInfo.objects.filter(id=id)
        print(team)
        teaminfo = TeamInfoSerializer(team, many=True)

        
        team_status=''
        for abc in teaminfo.data:
            if abc['team_memeber_1'] != '':
                mem_list.append(abc['team_memeber_1'])
            if abc['team_memeber_2'] != '':
                mem_list.append(abc['team_memeber_2'])
            if abc['team_memeber_3'] != '':
                mem_list.append(abc['team_memeber_3'])
            if abc['team_memeber_4'] != '':
                mem_list.append(abc['team_memeber_4'])
            if abc['status']==True:
                team_status='Qualified'
            else:
                team_status='Disqualified'
            team_details = {
                'id':abc['id'],
                'team_name':abc['team_name'],
                'idea':abc['idea'],
                'team_number':abc['team_number'],
                'team_leader':abc['team_leader'],
                'team_leader_phone':abc['team_leader_phone'],
                'team_mem':mem_list,
                'track':abc['track'],
                'status':team_status
            }
            break
        return Response(team_details,status=200)


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = UserType.objects.all()
        serializer=UserTypeSerializer(users,many=True)
        my_list=[]
        for i in serializer.data:
            data = {
                
                'userType':i['category'],
                'fullName':i['user']['first_name']+' '+i['user']['last_name'],
                'username':i['user']['username'],
                'user_id':i['user']['id']
            }
            my_list.append(data)

        resp = {
            'usersCount':len(my_list),
            'data':my_list
        }
        return Response(resp,status=200)


class AssignMember(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        
        mem_list = request.data['members']
        team_id = request.data['team_id']
        team = TeamInfo.objects.filter(id=team_id)[0]
        for i in mem_list:
            eval = UserType.objects.filter(user__id=i)[0]
            serializer = evaluator(team=team,evaluator_object=eval,round_level=ROUND_LEVEL)
            serializer.save()
        return Response({'status':'done'},status=200)
        