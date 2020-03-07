from django.contrib import admin

# Register your models here.
from . models import(
    TeamInfo,
    UserType,
    evaluator,
    Metrix,
    Notifications
)


admin.site.register(TeamInfo)
admin.site.register(UserType)
admin.site.register(evaluator)
admin.site.register(Metrix)
admin.site.register(Notifications)