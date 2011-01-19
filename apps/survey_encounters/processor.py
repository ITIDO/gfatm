import httplib, urllib
#from threading import Thread
from datetime import datetime
from django.contrib.gis.geos import Point

from reporters.models import Reporter
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
    
    # Check if the reporter is have a profile
    alias = data["data_interviewer"] #TODO: get reporter username from jr username tag
    print "++++++++++> %s" % (alias,)
    consent = data["data_consent_intervieweeconsent"]
    print '****************** %s' % (consent,)
    try:
        reporter = Reporter.objects.get(alias__iexact = alias)
        # make sure the reporter have a profile for a domain.
        # TODO: Limit the submission to a domain
        reporter_profile = ReporterProfile.objects.get(reporter=reporter)
        print "+++++++++++> %s" %(reporter,)
        # save a reporter with a profile
    except Exception, e:
        raise
    
#    form = Form()
    # check if consent was given or not and process
    in_form = Form()
    print '****************** %s' % (consent,)
    if  int(consent) == 1:
        # check if outlet exist
        o_name = data["data_outletname"]
        print "HEREEEEEEE"
        outlet = Outlets.objects.get(outlet_name__iexact = o_name)
        # if not create an outlet
        if outlet == []:
            print "HEREEEEEEE 2"
            outlet = Outlet()
            outlet.outlet_name = o_name
            outlet.owner_name = 'Mwenyeduka'
            outlet.type = data["data_outletType"]
            outlet.point = Point(-7.00,40.00)
            outlet.save()
        in_form.outlet = outlet
    else:
        # process deny submissions
        print "HEREEEEEEE else----"
    
    print "HEREEEEEEE 3"
    in_form.survey_user = reporter
    in_form.date_taken = datetime.now()
    in_form.save()
    print "HEREEEEEEE 4"
    print "Reporter -------------> %s" %(reporter,)
    print "FORM ----------> %s" % (in_form,)
#    return form

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
