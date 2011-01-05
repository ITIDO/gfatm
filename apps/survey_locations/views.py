from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

from rapidsms.webui.utils import render_to_response, paginated
from domain.decorators import login_and_domain_required

from survey_locations.models import Region, District, Village
from survey_locations.utils import _get_sort_info

@login_and_domain_required
def locations(request):
    template_name = 'locations-dashboard.html'
    
    r_columns = (('name','Regions'),)
    r_sort_column, r_sort_descending = _get_sort_info(request, default_sort_column="name",
                                                      default_sort_descending=False)
    r_sort_desc_string = "-" if r_sort_descending else ""
    
    d_columns = (('name','Districts'),)
    d_sort_column, d_sort_descending = _get_sort_info(request, default_sort_column="name",
                                                  default_sort_descending=False)
    d_sort_desc_string = "-" if d_sort_descending else ""
    
    # figure out where the request originated from
    r_search_string = request.REQUEST.get("qr", "")
    d_search_string = request.REQUEST.get("qd", "")
    v_search_string = request.REQUEST.get("qv", "")
    
    regions = Region.objects.order_by("%s%s" % (r_sort_desc_string, r_sort_column))
    districts = District.objects.order_by("%s%s" % (r_sort_desc_string, r_sort_column))

    if r_search_string == "":
        regions = regions.all()

    else:
        regions = regions.filter(
           Q(name__icontains=r_search_string) |
           Q(code__icontains=r_search_string))
    
    if d_search_string == "":
        districts = districts.all()

    else:
        districts = districts.filter(
           Q(name__icontains=r_search_string) |
           Q(code__icontains=r_search_string))

    regions = paginated(request, regions)
    districts = paginated(request, districts)
    return render_to_response(request, template_name, {"r_columns": r_columns,
                                                   "regions": regions,                                        
                                                   "r_sort_column": r_sort_column,
                                                   "r_sort_descending": r_sort_descending,
                                                   "r_search_string": r_search_string,
                                                   "d_columns": d_columns,
                                                   "districts": districts,                                        
                                                   "d_sort_column": d_sort_column,
                                                   "d_sort_descending": d_sort_descending,
                                                   "d_search_string": d_search_string
                                                   })

#@login_and_domain_required
#def region_list(request):
#    template_name = 'locations.html'
#    columns = (('name','Name'),
#               )
#    sort_column, sort_descending = _get_sort_info(request, default_sort_column="name",
#                                                  default_sort_descending=True)
#    sort_desc_string = "-" if sort_descending else ""
#    search_string = request.REQUEST.get("q", "")
#    
#    query = Region.objects.order_by("%s%s" % (sort_desc_string, sort_column))
#
#    if search_string == "":
#        query = query.all()
#
#    else:
#        query = query.filter(
#           Q(name__icontains=search_string) |
#           Q(code__icontains=search_string))
#
#    locations = paginated(request, query)
#    title = 'Regions'
#    return render_to_response(request, template_name, {"columns": columns,
#                                                   "locations": locations,
#                                                   "title": title,
#                                                   "sort_column": sort_column,
#                                                   "sort_descending": sort_descending,
#                                                   "search_string": search_string})
#
#@login_and_domain_required
#def district_list(request):
#    template_name = 'locations.html'
#    columns = (('name','Name'),
#               )
#    sort_column, sort_descending = _get_sort_info(request, default_sort_column="name",
#                                                  default_sort_descending=True)
#    sort_desc_string = "-" if sort_descending else ""
#    search_string = request.REQUEST.get("q", "")
#    
#    query = District.objects.order_by("%s%s" % (sort_desc_string, sort_column))
#
#    if search_string == "":
#        query = query.all()
#
#    else:
#        query = query.filter(
#           Q(name__icontains=search_string) |
#           Q(code__icontains=search_string))
#
#    locations = paginated(request, query)
#    title = 'Districts'
#    return render_to_response(request, template_name, {"columns": columns,
#                                                   "locations": locations,
#                                                   "title": title,
#                                                   "sort_column": sort_column,
#                                                   "sort_descending": sort_descending,
#                                                   "search_string": search_string})
#
#@login_and_domain_required
#def village_list(request):
#    template_name = 'locations.html'
#    columns = (('name','Name'),
#               )
#    sort_column, sort_descending = _get_sort_info(request, default_sort_column="name",
#                                                  default_sort_descending=True)
#    sort_desc_string = "-" if sort_descending else ""
#    search_string = request.REQUEST.get("q", "")
#    
#    query = Village.objects.order_by("%s%s" % (sort_desc_string, sort_column))
#
#    if search_string == "":
#        query = query.all()
#
#    else:
#        query = query.filter(
#           Q(name__icontains=search_string) |
#           Q(code__icontains=search_string))
#
#    locations = paginated(request, query)
#    title = 'Villages'
#    return render_to_response(request, template_name, {"columns": columns,
#                                                   "locations": locations,
#                                                   "title": title,
#                                                   "sort_column": sort_column,
#                                                   "sort_descending": sort_descending,
#                                                   "search_string": search_string})