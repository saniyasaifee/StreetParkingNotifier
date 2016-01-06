from django.db import models
from django.forms import ModelForm
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User

# Create your models here.
BOROUGH_CODE_CHOICES = (
  ('M', 'Manhattan'),
  ('K', 'Brooklyn'),
  ('B', 'Bronx'),
  ('S', 'Staten Island'),
  )

DIRECTION_CHOICES = (
  ('W', 'W'),
  ('E', 'E'),
  ('S', 'S'),
  ('N', 'N'),
  )

HOURS_CHOICES = (
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8),
  (9, 9),
  (10, 10),
  (11, 11),
  (12, 12),
  (13, 13),
  (14, 14),
  (15, 15),
  (16, 16),
  (17, 17),
  (18, 18),
  (19, 19),
  (20, 20),
  (21, 21),
  (22, 22),
  (23, 23),
  (24, 24),
  )

'''Car location module '''
class Location(models.Model):
    class Location(models.Model):
        #user = models.ForeignKey(User)
        user = models.CharField(max_length = 120, null = False, blank = False)
        latitude = models.DecimalField(max_digits = 30, decimal_places = 15, default = 0)
        longitude = models.DecimalField(max_digits = 30, decimal_places = 15, default = 0)
        boroughcode = models.CharField(max_length = 1, choices=BOROUGH_CODE_CHOICES, default = 'M', blank = False)
        main_street = models.CharField(max_length = 120, null = False, blank = False)
        from_street = models.CharField(max_length = 120, null = False, blank = False)
        to_street = models.CharField(max_length = 120, null=False, blank=False)
        direction = models.CharField(max_length = 1, choices = DIRECTION_CHOICES, null = False, blank = False)
        timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
        updated = models.DateTimeField(auto_now_add = False, auto_now = True)
        signid = models.CharField(max_length = 8)
        signdesc = models.CharField(max_length = 1024)
        hours = models.IntegerField(max_length = 2, choices = HOURS_CHOICES, default = 1)
        status = models.CharField(max_length = 1, default = 'O')

    def __unicode__(self):
        return smart_unicode(self.signdesc)
