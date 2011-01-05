from django.conf.urls.defaults import *
import survey_locations.views as views

urlpatterns = patterns('',    
    (r'^locations$', 'survey_locations.views.locations'),
#    (r'^districts$', 'survey_locations.views.district_list'),
#    (r'^regions$', 'survey_locations.views.region_list'),
#    (r'^villages$', 'survey_locations.views.village_list'),
)
