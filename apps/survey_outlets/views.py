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
def outlets(request):
    template_name="outlet_list.html"
    
    columns = (("outlet_name", "Outlet Name"),
               ("owner_name", "Owner"),
               ("join_date", "Joining Date"),
               )
    sort_column, sort_descending = _get_sort_info(request, default_sort_column="outlet_name",
                                                  default_sort_descending=False)
    sort_desc_string = "-" if sort_descending else ""
    search_string = request.REQUEST.get("q", "")
    query = Outlet.objects.order_by("%s%s" % (sort_desc_string, sort_column))
    
    if search_string == "":
       query = query.all()

    else:
        query = query.filter(
           Q(outlet_name__icontains=search_string) |
           Q(owner_name__icontains=search_string))

    outlets = paginated(request, query)
    context = {
               "outlets" : outlets,
               "columns": columns,
               "sort_column" : sort_column,
               "sort_descending" : sort_descending,
               "search_string" : search_string,
                }
    return render_to_response(request,template_name, context)

@login_and_domain_required
def outlet_details(request, pk):
    template_name = "outlet_details.html"
    
    outlet = Outlet.objects.get(id = pk);
    context = {
               'outlet' : outlet
               }
    return render_to_response(request, template_name, context)