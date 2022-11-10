from django.contrib import admin
from django.contrib.auth.models import User

from postproc.models import UserProfile


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username','genre_display', 'is_staff')

    def genre_display(self, obj) -> str:
        return obj.userprofile.genre

    genre_display.short_description = 'genre'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)