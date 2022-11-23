from django.contrib import admin


from django.contrib.auth.admin import UserAdmin as UserAdminModel
from django.contrib.auth.models import User

from postproc.models import UserProfile


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(UserAdminModel):
    inlines = (UserProfileInline, )
    list_display = ('username', 'id', 'genre_display', 'is_staff')

    def genre_display(self, obj) -> str:
        return obj.userprofile.genre

    genre_display.short_description = 'genre'

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        self.list_display = ('username','id','genre_display','is_staff')
        return super(UserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

