from django.contrib import admin
from account.models import User, ActivityPeriod


class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'username',  'is_admin', 'is_active', 'is_staff', 'is_superuser', 'real_name', 'tz')
    list_display = ('email', 'username',  'is_admin', 'is_active', 'is_staff', 'is_superuser', 'real_name', 'date_joined', 'last_login', 'uuid', 'tz')

class ActivityPeriodAdmin(admin.ModelAdmin):
    fields = ('user', 'start_time', 'end_time',)
    list_display = ('user', 'start_time', 'end_time', 'created_at', 'updated_at')



admin.site.register(User, UserAdmin)
admin.site.register(ActivityPeriod, ActivityPeriodAdmin)