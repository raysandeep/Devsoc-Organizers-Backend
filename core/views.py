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
    NotificationSerilizer,
    EvaluationParamsSerializer,
    TeamNamesSerializer
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
            list_of_teams = evaluator.objects.filter(evaluator_object__user=request.user).filter(round_level=1)
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
            'round':1,
            'data':not_completed_list,
            'completed_data':final_data_completed
        }
        return Response(data)

    
class Message(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if not request.data._mutable:
            request.data._mutable = True
            request.data['user']=request.user.id
            request.data['team']=TeamInfo.objects.filter(team_number=request.data['team'])[0].id
            request.data._mutable = False
            serializer = MessagingSerializer(data=request.data)
            push_service = FCMNotification(api_key="AIzaSyD8v3e4a3v-rcasU3Mh0KKkPaflm1dW1J4")
            if serializer.is_valid():
                serializer.save()
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
        evaluator1 = evaluator.objects.filter(id=request.data['evaluator']).filter(evaluator_object__user__id=request.user.id).filter(round_level=1)[0]
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
            evaluator1 = evaluator.objects.filter(id=request.data['eval_id']).filter(evaluator_object__user__id=request.user.id).filter(round_level=1)[0]
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