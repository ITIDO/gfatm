from django.conf.urls.defaults import *
import survey_reports.views as views

urlpatterns = patterns('',
    (r'^greports/$', 'survey_reports.views.reports'),
    (r'^greports/distribution/distributor/$', 'survey_reports.views.distribution_report'),
    (r'^greports/distribution/outlet/$', 'survey_reports.views.distribution_outlet_report'),
    (r'^greports/distribution/type/$', 'survey_reports.views.distribution_type_report'),
)

