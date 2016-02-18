from __future__ import unicode_literals

from django.db import models

# Create your models here.
class District(models.Model):
    district_name = models.CharField(max_length=100)
    activate = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True,db_index=True)
    superintendent = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return "%s District"% self.district_name


class School(models.Model)
    district = models.ForeignKey(District, blank=True, null=True)
    school_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True,db_index=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    grade_pk = models.BooleanField(default=False)
    grade_k = models.BooleanField(default=False)
    grade_1 = models.BooleanField(default=False)
    grade_2 = models.BooleanField(default=False)
    grade_3 = models.BooleanField(default=False)
    grade_4 = models.BooleanField(default=False)
    grade_5 = models.BooleanField(default=False)
    grade_6 = models.BooleanField(default=False)
    grade_7 = models.BooleanField(default=False)
    grade_8 = models.BooleanField(default=False)
    grade_9 = models.BooleanField(default=False)
    grade_10 = models.BooleanField(default=False)
    grade_11 = models.BooleanField(default=False)
    grade_12 = models.BooleanField(default=False)