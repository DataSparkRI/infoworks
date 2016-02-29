from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.utils.text import slugify

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
        
class SchoolDisplayData(models.Model):
    school_indicator = models.ForeignKey("SchoolIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionFor")
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.school_indicator, self.display)
       
class SchoolIndicatorData(models.Model):
    school_indicator_dataset = models.ForeignKey('SchoolIndicatorDataSet', blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_job = models.ForeignKey('dataimport.IndicatorFile', blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)
 
class SchoolIndicatorDataSet(models.Model):
    school_indicator = models.ForeignKey("SchoolIndicator", blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear)
    csv_file = models.FileField(upload_to="School_Indicator_Data", blank=True, null=True)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    @property
    def displaydata(self):
        index = SchoolDisplayData.objects.filter(school_indicator=self.school_indicator).values_list('display__name',flat=True).order_by("order")
        data = SchoolIndicatorData.objects.filter(school_indicator_dataset=self, dimension_x__in=index)
        result = []
        
        y_names = data.values("dimension_y").annotate(Count("dimension_y"))
        
        for i in y_names:
            result_data = []
            for a in index:
                try:
                    result_data.append(data.get(dimension_y=i["dimension_y"], dimension_x=a))
                except:
                    result_data.append(None)
            result.append({"dimension_y":i["dimension_y"],"data":result_data})
        return result
        
    @property
    def data(self):
        return SchoolIndicatorData.objects.filter(school_indicator_dataset=self)
        
    
    def __unicode__(self):
        return "%s - %s"%(self.school_indicator, self.school_year)

class SchoolIndicator(models.Model):
    school_indicator_set = models.ForeignKey('SchoolIndicatorSet', blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    order = models.IntegerField(default=0)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True)

    @property
    def dataset(self):
        return SchoolIndicatorDataSet.objects.filter(school_indicator=self).order_by("-school_year__school_year")

    @property
    def displaydata(self):
        return SchoolDisplayData.objects.filter(school_indicator=self).order_by("order")

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

class SchoolIndicatorSet(models.Model):
    school = models.ForeignKey("School", blank=True, null=True)
    title = models.CharField(max_length=100,blank=False)
    order = models.IntegerField(default=0)

    @property
    def indicators(self):
        return SchoolIndicator.objects.filter(school_indicator_set=self).order_by("order")

    def __unicode__(self):
        return "%s - %s"% (self.school.school_name, self.title)

class School(models.Model):
    district = models.ForeignKey("District", blank=True, null=True)
    school_code = models.CharField(max_length=100,unique=True)
    school_name = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    grade_type = models.CharField(max_length=100)
    principal = models.CharField(max_length=100, blank=True)
    
    activate = models.BooleanField(default=True)
    number_of_student = models.IntegerField(blank=True, null=True)
    number_of_teacher = models.IntegerField(blank=True, null=True)
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
    
    @property
    def indicatorset(self):
        return SchoolIndicatorSet.objects.filter(school=self).order_by("order")
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.school_name)
        super(School, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s (School)"% self.school_name


class DistrictDisplayData(models.Model):
    district_indicator = models.ForeignKey("DistrictIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionFor")
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.district_indicator, self.display)

class DistrictIndicatorData(models.Model):
    district_indicator_dataset = models.ForeignKey("DistrictIndicatorDataSet", blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_job = models.ForeignKey('dataimport.IndicatorFile', blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)

class DistrictIndicatorDataSet(models.Model):
    district_indicator = models.ForeignKey("DistrictIndicator", blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear)
    csv_file = models.FileField(upload_to="District_Indicator_Data", blank=True, null=True)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    @property
    def displaydata(self):
        index = DistrictDisplayData.objects.filter(district_indicator=self.district_indicator).values_list('display__name',flat=True).order_by("order")
        data = DistrictIndicatorData.objects.filter(district_indicator_dataset=self, dimension_x__in=index)
        result = []
        
        y_names = data.values("dimension_y").annotate(Count("dimension_y"))
        
        for i in y_names:
            result.append({"dimension_y":i["dimension_y"],"data":[ data.get(dimension_y=i["dimension_y"], dimension_x=a) for a in index]})
        return result
        
    @property
    def data(self):
        return DistrictIndicatorData.objects.filter(district_indicator_dataset=self)
    
    def __unicode__(self):
        return "%s - %s"%(self.district_indicator, self.school_year)


class DistrictIndicator(models.Model):
    district_indicator_set = models.ForeignKey('DistrictIndicatorSet', blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    order = models.IntegerField(default=0)
    short_title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    data_indeicator = models.BooleanField(default=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True)

    @property
    def dataset(self):
        return DistrictIndicatorDataSet.objects.filter(district_indicator=self).order_by("-school_year__school_year")

    @property
    def displaydata(self):
        return DistrictDisplayData.objects.filter(district_indicator=self).order_by("order")

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


class DistrictIndicatorSet(models.Model):
    district = models.ForeignKey("District")
    title = models.CharField(max_length=100,blank=False)
    order = models.IntegerField(default=1)

    @property
    def indicators(self):
        return DistrictIndicator.objects.filter(district_indicator_set=self).order_by("order")
        
        
    def __unicode__(self):
        return "%s - %s"% (self.district.district_name, self.title)
        
class District(models.Model):
    district_name = models.CharField(max_length=100)
    district_code = models.CharField(max_length=100,unique=True)
    activate = models.BooleanField(default=True)
    number_of_student = models.IntegerField(blank=True, null=True)
    number_of_teacher = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True,db_index=True)
    superintendent = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    indicator_modified = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.district_name)
        super(District, self).save(*args, **kwargs)
    
    @property
    def indicatorset(self):
        return DistrictIndicatorSet.objects.filter(district=self).order_by("order")
    
    @property
    def schools(self):
        return School.objects.filter(district=self, activate=True).order_by("school_name")
    
    def __unicode__(self):
        return "%s (District)"% self.district_name

        


        
        
        
        
