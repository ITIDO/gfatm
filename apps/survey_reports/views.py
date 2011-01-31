import logging
import hashlib
import settings
import traceback
import sys
import os
import uuid
import string
from datetime import timedelta

from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.exceptions import *
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict
from django.db import transaction
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson

from rapidsms.webui.utils import render_to_response, paginated

from xformmanager.models import *
from hq.models import *
from graphing import dbhelper
from graphing.models import *
from receiver.models import *
from domain.decorators import login_and_domain_required, domain_admin_required
from program.models import Program
from phone.models import PhoneUserInfo
    
import hq.utils as utils
import hq.reporter as reporter
import hq.reporter.custom as custom
import hq.reporter.metastats as metastats

import hq.reporter.inspector as repinspector
import hq.reporter.metadata as metadata

from reporters.utils import *
from reporters.views import message, check_reporter_form, update_reporter
from reporters.models import Reporter, PersistantBackend, PersistantConnection

from survey_outlets.models import Outlet
from survey_outlets.utils import _get_sort_info

@login_and_domain_required
def reports(request):
    template_name = "reports.html"
    
    context = {}
    return render_to_response(request, template_name, context)

def report_render(request, report_name = None, heading =None, columns = None, values = None):
    '''
        Render reports given
        @param request: 
        @param report_name: Name of the report
        @param heading: Heading of the report
        @param columns: Columns for the report table list
        @param values: values 
            e.g. values = [[
                          ['row_heading',value1,value2,],
                        ]]
    '''
    template_name = "actual_report.html"
    context = {
           'report' : report_name,
           'heading' : heading,
           'columns' : columns,
           'values' : values,
           }
    return render_to_response(request, template_name, context)


@login_and_domain_required
def distribution_report(request):
    report_name = 'Distribution Report'
    h1 = 'Number of ACT Distributors in Tanzania'
    columns = [
                'Type', 
                'Number', 
                '% Proportion',
            ]
               
    

    values = [
           ['Front Line',4,3.3,],
           ['Reginal',56,47.5,],
           ['District',60,49.2,],
           ['Total',122,100,],
        ]
            
    return report_render(request, report_name, h1, columns, values )

@login_and_domain_required
def distribution_outlet_report(request):
    report_name = 'Distribution Report'
    h1 = 'Number of ACT outlets in Tanzania'
    columns = [
            'Name of District', 
            'Pharmacy', 
            'Hospital',
            'Health Center',
            'Dispensary',
            'ADDO',
            'DLDB',
            'TOTAL'
            ]

    values = [
           ['Kinondoni',4,3.3,0,4,5,6,7,],
           ['Reginal',56,47.5,1,4,6,7,0,],
           ['District',60,49.2,34,76,23,67,23],
           ['Total',122,100,44,56,34,67,67,],
       ]
    return report_render(request, report_name, h1, columns, values )


@login_and_domain_required
def distribution_type_report(request):
    report_name = 'Distribution Report'
    h1 = 'Number of ACT outlets in Tanzania: Outlets types'
    columns = [
            'Outlet Type',
            'Number',
            '%',
            ]

    values = [
           ['ADDO',4,3.3,],
           ['DLDB',56,47.5,],
           ['Dispensary',60,49.2,],
           ['Pharmacy',60,49.2,],
           ['Health Center ',60,49.2,],
           ['Hospital',60,49.2,],
           ['Total',122,100,],
       ]
    return report_render(request, report_name, h1, columns, values )