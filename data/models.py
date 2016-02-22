from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


DATA_TYPE_CHOICES = (
    ('NUMERIC', 'numeric'),
    ('STRING', 'string'),
)

# Create your models here.
class IndicatorTitle(models.Model):
    title = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s"% self.title

class SchoolYear(models.Model):
    school_year = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s"% self.school_year

class District(models.Model):
    district_name = models.CharField(max_length=100)
    district_code = models.CharField(max_length=100,unique=True)
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
    indicator_modified    = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s District"% self.district_name

class DistrictNumberOfStudentAndTeacher(models.Model):
    district = models.ForeignKey(District)
    activate = models.BooleanField(default=False)
    school_year = models.ForeignKey(SchoolYear)
    student = models.IntegerField(null=True)
    teacher = models.IntegerField(null=True)
    school = models.IntegerField(null=True)
    
    def __unicode__(self):
        return "%s - [ %s students and %s teachers]"% (self.school_year, self.student, self.teacher)

class DistrictIndicatorSet(models.Model):
    district = models.ForeignKey(District)
    title = models.CharField(max_length=100,blank=False)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s - %s"% (self.district.district_name, self.title)
        
class DistrictIndicator(models.Model):
    district_indicator_set = models.ForeignKey(DistrictIndicatorSet, blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.district_indicator_set.district.indicator_modified = timezone.now()
        self.district_indicator_set.district.save()
        return super(DistrictIndicator, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s - %s"% (self.district_indicator_set, self.title)

class DistrictIndicatorDataSet(models.Model):
    district_indicator = models.ForeignKey(DistrictIndicator, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear)
    csv_file = models.FileField(upload_to="District_Indicator_Data", blank=True, null=True)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    def __unicode__(self):
        return "%s - %s"%(self.district_indicator, self.school_year)

class DistrictIndicatorData(models.Model):
    district_indicator_dataset = models.ForeignKey(DistrictIndicatorDataSet, blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_job =  models.ForeignKey('dataimport.IndicatorFile', blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)


class School(models.Model):
    district = models.ForeignKey(District, blank=True, null=True)
    school_code = models.CharField(max_length=100,unique=True)
    school_name = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    grade_type = models.CharField(max_length=100)
    principal = models.CharField(max_length=100, blank=True)
    
    activate = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True,db_index=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    elementary_school = models.BooleanField(default=False)
    middle_school = models.BooleanField(default=False)
    high_school = models.BooleanField(default=False)
    
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
    indicator_modified = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s School"% self.school_name
        
class SchoolNumberOfStudentAndTeacher(models.Model):
    school = models.ForeignKey(School)
    activate = models.BooleanField(default=False)
    school_year = models.ForeignKey(SchoolYear)
    student = models.IntegerField(null=True)
    teacher = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s - [ %s students and %s teachers]"% (self.school_year, self.student, self.teacher)
        

class SchoolIndicatorSet(models.Model):
    school = models.ForeignKey(School, blank=True, null=True)
    title = models.CharField(max_length=100,blank=False)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s - %s"% (self.school.school_name, self.title)
        
class SchoolIndicator(models.Model):
    school_indicator_set = models.ForeignKey(SchoolIndicatorSet, blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.school_indicator_set.school.indicator_modified = timezone.now()
        self.school_indicator_set.school.save()
        return super(SchoolIndicator, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"% (self.school_indicator_set, self.title)

class SchoolIndicatorDataSet(models.Model):
    school_indicator = models.ForeignKey(SchoolIndicator, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear)
    csv_file = models.FileField(upload_to="School_Indicator_Data", blank=True, null=True)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    def __unicode__(self):
        return "%s - %s"%(self.school_indicator, self.school_year)

class SchoolIndicatorData(models.Model):
    school_indicator_dataset = models.ForeignKey(SchoolIndicatorDataSet, blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_job =  models.ForeignKey('dataimport.IndicatorFile', blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)
        
        
        
        