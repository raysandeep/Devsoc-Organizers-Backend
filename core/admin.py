from django.contrib import admin

# Register your models here.
from . models import(
    TeamInfo,
    UserType,
    evaluator,
    EvaluationParms,
    Notifications,
    Messaging
)

admin.site.register(EvaluationParms)
admin.site.register(TeamInfo)
admin.site.register(UserType)
admin.site.register(evaluator)
admin.site.register(Notifications)
admin.site.register(Messaging)