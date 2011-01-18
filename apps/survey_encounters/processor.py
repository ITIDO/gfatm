import httplib, urllib
#from threading import Thread
from datetime import datetime
from django.contrib.gis.geos import Point

from hq.models import ReporterProfile

def add_encounter(sender, instance, created, **kwargs): #get sender, instance, created
    """ Adds survey encounters submission from xforms to database """
    # only process newly created forms, not all of them
    if not created: return
    print ">>>>>>>>>>> FORMS ;-) <<<<<<<<<<<<<<<"
    
    # check the form type to see if it is a new sample
    form_xmlns = instance.formdefmodel.target_namespace
    data = instance.formdefmodel.row_as_dict(instance.raw_data)

    form = create_form(data)
#    add_data(data, form)
    
def create_form(data):
    """ Create a form for submitted xform """
    print " [[[[ CREATE FORM ]]]]] "

    # TODO: check if outlet is in db else create the outlet
#    o_name =  data[data_outlet]
#    if o_name:
#        outlet = Outlet.objects.get(outlet_name__iexact = o_name)
#    else:
#        outlet = Outlet(outlet_name = o_name,
#                        owner_name = "Aptana",
#                        point = Point(-7.00, 40.00)
#                        ).save()
    print "Outlet -----> %s" % ("outlet",)
    # Check if the reporter is have a profile
    alias = sample_data["data_interviewer"] #TODO: get reporter username from jr username tag
    try:
        reporter = Reporter.objects.get(alias__iexact = alias)
        # make sure the reporter have a profile for a domain.
        # TODO: Limit the submission to a domain
        reporter_profile = ReporterProfile.objects.get(reporter=reporter)
        # save a reporter with a profile
    except Exception, e:
        raise
    
    print "Reporter -------------> %s" %(reporter,)
    # create form
    form =Form(
                outlet = outlet,
                survey_user = reporter,
                date_taken = datetime.now(),
                ).save()
    print "----------> %s" % (form,)
    return form

def add_data(data_list, form):   
    """ Add field data to answers and links questionaire qn to submits """ 
    # take each data from list and match with a Question
    for data in data_list:
        try:
            # get question
            qn = Question.objects.get(xmlPath=data)
            
            # store answer
            answer = Answer()
            answer.answer = data_list[data]
            answer.save()
            
            # link qn and answer
            QALink(
                   question = qn,
                   answer = answer,
                   form = form,
                   ).save()
        except Exception, e:
            raise

# testing 
def test(sender, instance, created, **kwargs):
    print ">>>>TESTING DJANGO SIGNALS<<<<<"
