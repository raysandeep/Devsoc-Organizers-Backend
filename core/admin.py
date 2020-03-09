from django.contrib import admin

# Register your models here.
from . models import(
    TeamInfo,
    UserType,
    evaluator,
    EvaluationParms,
    Notifications
)

admin.site.register(EvaluationParms)
admin.site.register(TeamInfo)
admin.site.register(UserType)
admin.site.register(evaluator)
admin.site.register(Notifications)