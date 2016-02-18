from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


DATA_TYPE_CHOICES = (
    ('numeric', 'numeric'),
    ('string', 'string'),
)

# Create your models here.
class IndicatorTitle(models.Model):
    title = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s"% self.title


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
    modified    = models.DateTimeField(blank=True)
    
    def __unicode__(self):
        return "%s District"% self.district_name

class DistrictNumberOfStudentAndTeacher(models.Model):
    district = models.ForeignKey(District)
    school_year = models.CharField(max_length=100,blank=False,unique=True)
    student = models.IntegerField(null=True)
    teacher = models.IntegerField(null=True)
    school = models.IntegerField(null=True)
    
    def __unicode__(self):
        return "%s - [ %s students and %s teachers]"% (self.school_year, self.student, self.teacher)

class DistrictIndicatorSet(models.Model):
    district = models.ForeignKey(District)
    title = models.CharField(max_length=100,blank=False,unique=True)

    def __unicode__(self):
        return "%s %s"% (self.district.district_name, self.title)
        
class DistrictIndicator(models.Model):
    district_indicator_set = models.ForeignKey(DistrictIndicatorSet, blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    school_year = models.CharField(max_length=100,blank=False)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.district_indicator_set.district.modified = timezone.now()
        return super(DistrictIndicator, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s - %s"% (self.district_indicator_set, self.title)

class DistrictIndicatorData(models.Model):
    district_indicator = models.ForeignKey(DistrictIndicator, blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)


class School(models.Model):
    district = models.ForeignKey(District, blank=True, null=True)
    school_name = models.CharField(max_length=100)
    activate = models.BooleanField(default=True)
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
    modified    = models.DateTimeField(blank=True)
    
    def __unicode__(self):
        return "%s School"% self.school_name
        
class SchoolNumberOfStudentAndTeacher(models.Model):
    school = models.ForeignKey(School)
    school_year = models.CharField(max_length=100,blank=False,unique=True)
    student = models.IntegerField(null=True)
    teacher = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s - [ %s students and %s teachers]"% (self.school_year, self.student, self.teacher)
        

class SchoolIndicatorSet(models.Model):
    school = models.ForeignKey(School, blank=True, null=True)
    title = models.CharField(max_length=100,blank=False,unique=True)

    def __unicode__(self):
        return "%s %s"% (self.school.school_name, self.title)
        
class SchoolIndicator(models.Model):
    school_indicator_set = models.ForeignKey(SchoolIndicatorSet, blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    school_year = models.CharField(max_length=100,blank=False)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.school_indicator_set.school.modified = timezone.now()
        return super(SchoolIndicator, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s - %s"% (self.school_indicator_set, self.title, self.school_year)

class SchoolIndicatorData(models.Model):
    school_indicator = models.ForeignKey(SchoolIndicator, blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)
        
        
        
        