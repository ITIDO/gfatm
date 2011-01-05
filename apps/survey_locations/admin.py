from django.contrib import admin

from survey_locations.models import Region, District, Village

admin.site.register(Region)

class DistrictAdmin(admin.ModelAdmin):
    search_fields = ('name','code',)
admin.site.register(District, DistrictAdmin)

class VillageAdmin(admin.ModelAdmin):
    search_fields = ('name','code',)
admin.site.register(Village,VillageAdmin)