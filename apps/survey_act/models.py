from django.db import models

class Type(models.Model):
    ''' subsidesed act types '''
    name = models.CharField(max_length = 126)
    
    def __unicode__(self):
        return '%s' % (self.name,)
    
class Manufacture(models.Model):
    ''' brand manufacture '''
    name = models.CharField(max_length = 126)
    
    def __unicode__(self):
        return '%s' % (self.name,)

class SubsidisedAct(models.Model):
    ''' sub-sidised ACTS '''
    description = models.TextField()
    manufacture = models.ForeignKey(Manufacture)
    type = models.ForeignKey(Type)
#BRAND_NAME
#GENERIC NAME
#MANUFACTURE
    def __unicode__(self):
        return '%s - %s' % (self.description[:15], self.type) #just return part of description
