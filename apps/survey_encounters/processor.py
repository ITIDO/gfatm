import httplib, urllib
from threading import Thread
from datetime import datetime

from django.db.models.signals import post_save

from xformmanager.models import Metadata
from reporters.models import Reporter

from survey_encounters.models import Question, Answer, Form, QALink

def add_encounter(sender, instance, created, **kwargs): #get sender, instance, created
    """ Adds survey encounters submission from xforms to database """
    # only process newly created forms, not all of them
    if not created: return
#    print ">>>>>>>>>>> FORMS <<<<<<<<<<<<<<<"
    # check the form type to see if it is a new sample
    form_xmlns = instance.formdefmodel.target_namespace
    data = instance.formdefmodel.row_as_dict(instance.raw_data)
    
    form = create_form(data)
    add_data(data, form)
    
def create_form(data):
    """ Create a form for submitted xform """
    f_date = data["gfatm_data_assessment_assessmentdate"]
    
    region = Region.objects.get(name = data["gfatm_data_region"])
    district = District.objects.get(name = data["gfatm_data_district"])
    #TODO: get outlet / create outlet
    outlet = Outlet.objects.get(name = data["gfatm_data_outlet"])
    
    #get user(reporter)
    alias = sample_data["gfatm_data_username"]
    try:
        reporter = Reporter.objects.get(alias__iexact = alias)
        # make sure the reporter have a profile for a domain.
        # TODO: Limit the submission to a domain
        reporter_profile = ReporterProfile.objects.get(reporter=reporter)
        # save a reporter with a profile
        sample.taken_by = reporter
    except Exception, e:
        raise
    #save form
    Form(
         region = region,
         district = district,
         outlet = outlet,
         survey_user = alias,
         date_taken = f_date,
         ).save()
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
 

# Register to receive signals each time a Metadata is saved    
#post_save.connect(add_encounter, sender=Metadata)