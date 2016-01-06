# -*- coding: utf-8 -*-
from django.db import models

from django.utils.encoding import smart_unicode

# Create your models here.
class ShowMap(models.Model):
    user_id = models.CharField(max_length=120, null=True, blank=True)
    latitude = models.CharField(max_length=120, null=True, blank=True)
    longitude = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.user_id)