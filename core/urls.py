from django.conf.urls import url
from django.urls import path,include
from . import views

urlpatterns = [
    url(r"^token/login/?$", views.TokenCreateView.as_view(), name="login"),
    path('list/',views.EvaluatorList.as_view(),name="list"),
]