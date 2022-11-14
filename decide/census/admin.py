from django.contrib import admin

from .models import Census,CensusGroup


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id','group')
    list_filter = ('voting_id', 'group')
    raw_id_fields = ('group',)

    search_fields = ('voter_id', 'group')

class CensusGroupAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    
    search_fields = ('name',)


admin.site.register(Census, CensusAdmin)
admin.site.register(CensusGroup, CensusGroupAdmin)
