from django.db import models
from django.contrib.auth.models import AbstractUser, Group , Permission
from django.utils.translation import gettext as _

class Facility_staff(AbstractUser):
    # Add any additional fields here
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='facility_staff_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='facility_staff_set')


class Hdss_staff(AbstractUser):
    # Add any additional fields here
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='hdss_staff_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='hdss_staff_set')



class SyntheticFacilityV3(models.Model):
    recnr = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    petname = models.CharField(max_length=255)
    dob = models.DateField()
    sex = models.CharField(max_length=1)
    nationalid = models.CharField(max_length=255)
    patientid = models.CharField(max_length=255)
    visitdate = models.DateField()

    class Meta:
        app_label = 'record_app'
        managed = False
        db_table = 'synthetic_facility_v3'

class SyntheticHdssV3(models.Model):
    recnr = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    petname = models.CharField(max_length=255)
    dob = models.DateField()
    sex = models.CharField(max_length=1)
    nationalid = models.CharField(max_length=255)
    hdssid = models.CharField(max_length=255)
    hdsshhid = models.CharField(max_length=255)

    class Meta:
        app_label = 'record_app'
        managed = False
        db_table = 'synthetic_hdss_v3'