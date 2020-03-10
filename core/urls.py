from django.conf.urls import url
from django.urls import path,include
from . import views
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

urlpatterns = [
    url(r"^token/login/?$", views.TokenCreateView.as_view(), name="login"),
    path('list/',views.EvaluatorList.as_view(),name="list"),
    path('message/',views.Message.as_view(),name="Message"),
    path('register/',views.NotificationView.as_view(),name="Message"),
    path('evaluvate/',views.EvaluateView.as_view(),name="eval"),
    path('team/names/',views.GetTeamNames.as_view(),name="teams"),
    path('team/info/<str:id>/',views.GetTeamInfo.as_view(),name="team-info"),
    url(r'^auth/', include('djoser.urls')),
]


