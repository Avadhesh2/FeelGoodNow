from django.contrib import admin
from .models import IdealData, UserData


@admin.register(IdealData)
class IdealDataAdmin(admin.ModelAdmin):
    list_display = ('age', 'gender', 'height',
                    'weight', 'sleeping_hours', 'bmi')
    readonly_fields = ('bmi',)


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('weight', 'gender', 'height',
                    'activity_level', 'sleeping_hours', 'age')


#youtube
from .models import Video, UserProfile

admin.site.register(Video)
admin.site.register(UserProfile)    