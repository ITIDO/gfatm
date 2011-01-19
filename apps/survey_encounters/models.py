from datetime import datetime

from django.db import models
from django.db.models.signals import post_save

from xformmanager.models import Metadata


from reporters.models import Reporter

from survey_outlets.models import Outlet
from survey_locations.models import Region, District
#from survey_encounters.processor import add_encounter
import httplib, urllib
from threading import Thread
#from datetime import datetime
from django.contrib.gis.geos import Point

#from reporters.models import Reporter
from hq.models import ReporterProfile



class Question(models.Model):
    '''
        A question asked in the field during the survey
    '''    
    question = models.CharField(max_length = 256)
    answer_type = models.CharField(max_length = 10,)
    xmlPath = models.CharField(max_length = 256)
    date_added = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.question,)

class Answer(models.Model):
    '''
        Answers to the questions.
        this class will be populated as data is submitted via mobile phone
    '''
    answer = models.CharField(max_length = 256)
    date_recieved = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.answer)

class Form(models.Model):
    '''
        submitted form data
    '''
    date_received = models.DateTimeField(default = datetime.now)
    date_taken = models.DateTimeField()
    survey_user = models.ForeignKey(Reporter)
    outlet = models.ForeignKey(Outlet, null=True, blank=True)
    # datetime for form save
    
    def __unicode__(self):
        if self.outlet:
            d = '%s : %s' % (self.outlet.outlet_name, self.date_received)
        else:
            d = 'None : %s' % (self.date_received)
        return d

class QALink(models.Model):
    ''' Links questions to answers on a form '''
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    form = models.ForeignKey(Form)
    
    def __unicode__(self):
        return 'Form %s : Q %s - A %s' % (self.form, self.question, self.answer)
    




def add_encounter(sender, instance, created, **kwargs): #get sender, instance, created
    """ Adds survey encounters submission from xforms to database """
    # only process newly created forms, not all of them
    if not created: return
    print ">>>>>>>>>>> FORMS ;-) <<<<<<<<<<<<<<<"
    
    # check the form type to see if it is a new sample
    form_xmlns = instance.formdefmodel.target_namespace
    data = instance.formdefmodel.row_as_dict(instance.raw_data)

    form = create_form(data)
    thread = Thread( target = add_data, args =(data, form))
    thread.start()
    
def create_form(data):
    """ Create a form for submitted xform """
    # Check if the reporter is have a profile
    alias = data["data_interviewer"] #TODO: get reporter username from jr username tag
    consent = data["data_consent_intervieweeconsent"]
    try:
        reporter = Reporter.objects.get(alias__iexact = alias)
        # make sure the reporter have a profile for a domain.
        # TODO: Limit the submission to a domain
        reporter_profile = ReporterProfile.objects.get(reporter=reporter)
        # save a reporter with a profile
    except Exception, e:
        raise
    
    # check if consent was given or not and process
    in_form = Form()
    if  int(consent) == 1:
        # check if outlet exist
        o_name = data["data_outletname"]
        outlet = Outlets.objects.get(outlet_name__iexact = o_name)
        # if not create an outlet
        if outlet == []:
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
    
    in_form.survey_user = reporter
    in_form.date_taken = datetime.now()
    in_form.save()
    
    return in_form

def add_data(data_list, form):   
    """ Add field data to answers and links questionare qn to submits """ 
    # take each data from list and match with a Question
    # create a list of only tags with actual data reference
    data = []
    IGNORE = ['id', 
              'data interviewer', 
              'data_region', 
              'data_district', 
              'data_village', 
              'data_location',
              ]
    for d in data_list:
        if data_list[d] != None:
            if not d in IGNORE:
                data.append(d)
                
    qns = Question.objects.filter(xmlPath__in = data)
    for d in data:
        # get question
        for qn in qns:
            if qn.xmlPath == d: 
                # store answer
                answer = Answer()
                answer.answer = data_list[d]
                answer.save()
                
                # link questions and answer
                QALink(
                       question = qn,
                       answer = answer,
                       form = form,
                       ).save()
                break


def test(sender, instance, created, **kwargs):
    ''' testing django signal actually works '''
    print ">>>>TESTING DJANGO SIGNALS<<<<<"



# Register to receive signals each time a Metadata is saved    
post_save.connect(add_encounter, sender=Metadata)