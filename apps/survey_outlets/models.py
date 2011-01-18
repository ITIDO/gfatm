from datetime import datetime

from django.db import models
from django.contrib.gis.db import models
from survey_locations.models import Village

class OutletType(models.Model):
    '''
        Outlet category definition
    '''
    name = models.CharField(max_length = 126)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s' % (self.name)

class Outlet(models.Model):
    '''
        Are medical store, which sales malaria medicine to the public
    '''
    outlet_name = models.CharField(max_length = 126)
    owner_name = models.CharField(max_length = 126)
    join_date = models.DateTimeField(default = datetime.now)
    exit_date = models.DateTimeField(null=True, blank=True)
    strutam = models.CharField(max_length = 126, null=True)
    type = models.ForeignKey(OutletType, null=True)
    village = models.ForeignKey(Village, null=True)
    point = models.PointField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return '%s' % (self.outlet_name)
#tel_phone
#district
#contacts
# dispenser name,
# types; ADDO, DLDB, PHARMACY, HEALTHY CENTER, DISPENSARY, HOSPITAL, 
