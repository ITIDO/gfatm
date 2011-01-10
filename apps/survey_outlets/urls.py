from django.conf.urls.defaults import *
import survey_outlets.views as views

urlpatterns = patterns('',
    (r'^outlets$', 'survey_outlets.views.outlets'),
    (r'^outlets/(?P<pk>\d+)/details$', 'survey_outlets.views.outlet_details'),
)