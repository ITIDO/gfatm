from datetime import datetime

from django.db import models

class Region(models.Model):
    '''
        Holds all the geographical regions within a country
    '''
    name = models.CharField(max_length = 126)
    code = models.CharField(max_length = 12, blank = False)
    created_date = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    def districts(self):
        '''
            Returns all the districts in a region.
        '''
        d = District.objects.filter(region__id = self.id)
        return d

class District(models.Model):
    '''
        sub-division on the regions
    '''
    name = models.CharField(max_length = 126)
    code = models.CharField(max_length = 12, blank = False)
    region = models.ForeignKey(Region)
    created_date = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
class Village(models.Model):
    '''
        division within a district
    '''
    name = models.CharField(max_length = 126)
    code = models.CharField(max_length = 12, blank = False)
    district = models.ForeignKey(District)
    created_date = models.DateTimeField(default = datetime.now)
    
    def __unicode__(self):
        return '%s' % self.name

