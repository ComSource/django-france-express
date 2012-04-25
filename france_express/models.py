# -*- coding: utf-8 *-*

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal
import types
from france_express.config import *

class Offer(models.Model):
    
    name = models.CharField(_("France Express offer name"), max_length=50)

class Zone(models.Model):

    name = models.CharField(_("Zone name for the related offer"), max_length=255)
    offer = models.ForeignKey(Offer)

    def __repr__(self):
        return self.name

class Department(models.Model):
    
    number = models.IntegerField(max_length=3)
    zone = models.ForeignKey(Zone)

class Rate(models.Model):
    
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    zone = models.ForeignKey(Zone)

    def __repr__(self):
        return "<Rate: max %.2fkg (%s) %.2f EUR>" % (self.weight, self.zone.name, self.price)
    
    @staticmethod
    def get_rates(department_number, weight):
        
        if type(department_number) != types.IntType:
            raise TypeError, "Country must be a string, not %s" % type(country)
        
        if type(weight) != types.FloatType and type(weight) != types.IntType:
            raise TypeError, "Weight must be a float"
        
        if weight < 0 or weight > FRANCE_EXPRESS_MAX_WEIGHT:
            raise ValueError, "FranceExpress only supports 0 < weight < %d" % FRANCE_EXPRESS_MAX_WEIGHT
        
        rs = []
        for zone in [ d.zone for d in Department.objects.filter(number=department_number) ]:
            w = Rate.objects.filter(weight__gte=Decimal(str(weight)), zone=zone)[0].weight
            rs.append(Rate.objects.get(weight=w, zone=zone))
            
        return sorted(rs, key=lambda rate: rate.price)

    class Meta:
        unique_together = (('weight', 'price', 'zone'))
