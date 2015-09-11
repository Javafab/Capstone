from django.contrib import admin
from .models import MakeUser, RecordTime


class MakeUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(MakeUser, MakeUserAdmin)


class RecordTimeAdmin(admin.ModelAdmin):
    pass
admin.site.register(RecordTime, RecordTimeAdmin)
