from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

'''this is the method to validate the phone number field'''
def phoneNumber_validate(phoneNumber):
    if len(phoneNumber) == 10:
        try:
            int(phoneNumber)
        except:
            raise ValidationError("You can input only numbers in this field")
    else:
        raise ValidationError("The value in this field has to be 10 digit long")

'''This is class is ised to extend the user model to add Phone number'''
class UserProfile(models.Model):

    user = models.OneToOneField(User)
    phoneNumber = models.CharField(max_length=10, blank=True, null=True, validators=[phoneNumber_validate])

    def __unicode__(self):
        return u"Profile for %s" % self.user
