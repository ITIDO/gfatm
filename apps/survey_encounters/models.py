from datetime import datetime

from django.db import models

from reporters.models import Reporter

from survey_outlets.models import Outlet
from survey_locations.models import Region, District


class Question(models.Model):
    '''
        A question asked in the field during the survey
    '''
    ANSWER_TYPES = (
                    ('num', 'Number'),
                    ('word', 'Word'),
                    ('brand', 'BrandName'),
                    ('providers', 'Providers'),
                    )
    
    question = models.CharField(max_length = 256)
    xmlPath = models.CharField(max_length = 256)
    answer_type = models.CharField(max_length = 10, choices=ANSWER_TYPES)
    date_added = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.question,)

class Answer(models.Model):
    '''
        Answers to the questions.
        this class will be populated as data is submitted via mobile phone
    '''
    ANSWER_CHOICES = {
                        'brand': {
                                1 : 'BrandA',
                                2 : 'BrandB',
                                },
                        'provider' : {
                                      1 : 'owner',
                                      2 : 'doctor',
                                      },
                      }
    
    answer = models.CharField(max_length = 256)
    date_recieved = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.answer)

class Form(models.Model):
    '''
        submitted form data
    '''
    date_received = models.DateTimeField(default = datetime.now)
    date_taked = models.DateTimeField()
    survey_user = models.ForeignKey(Reporter)
    region = models.ForeignKey(Region)
    district = models.ForeignKey(District)
    outlet = models.ForeignKey(Outlet)
    
    def __unicode__(self):
        d = '%s : %s' % (self.outlet.outlet_name, self.date_received)
        return d

class QALink(models.Model):
    ''' Links questions to answers on a form '''
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    form = models.ForeignKey(Form)
    
    def __unicode__(self):
        return 'Form %s : Q %s - A %s' % (self.form, self.question, self.answer)