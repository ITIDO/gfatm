def _get_sort_info(request, default_sort_column, default_sort_descending):
    sort_column = default_sort_column
    sort_descending = default_sort_descending
    if "sort_column" in request.GET:
        sort_column = request.GET["sort_column"]
    if "sort_descending" in request.GET:
        if request.GET["sort_descending"].startswith("f"):
            sort_descending = False
        else:
            sort_descending = True
    return (sort_column, sort_descending)


#def add_outlet(name, lng, lat):
#    o = Outlet()
#    o.outlet_name = name
#    o.outlet_owner = "null"
#    o.point = Point(lng,lat)
#    o.save()
#
#
#from xlrd import open_workbook
#wb = open_workbook('/home/allen/Desktop/moro.xls')
#s = wb.sheet_by_index(1)
#for row in range(s.nrows):
#    values = []
#    for col in range(3,7):
#        values.append(s.cell(row,col).value)
#    name = values[0]
#    lat = values[1]
#    lng = values[2]
#    if name != "interviewer_outlet" :
#        if lat != 'null':
#            if lng != 'null':
#                lat = float(lat)
#                lng = float(lng)
#                add_outlet(name,lng,lat)
#                print "%s (%s, %s)" % (name, lat, lng)
