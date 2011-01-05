from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap

from survey_outlets.models import OutletType, Outlet
#TODO: 
#    move the Google Map API key to settings file
#    create template directory for admin customization
GMAP = GoogleMap(key='ABQIAAAAwLx05eiFcJGGICFj_Nm3yxSy7OMGWhZNIeCBzFBsFwAAIleLbBRLVT87XVW-AJJ4ZR3UOs3-8BnQ-A')

admin.site.register(OutletType)

class OutletAdmin(admin.OSMGeoAdmin):
#    extra_js = [GMAP.api_url + GMAP.key]
#    map_template = 'gis/admin/google.html'
    search_fields = ('name','code')
admin.site.register(Outlet,OutletAdmin)
