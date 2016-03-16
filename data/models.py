from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import csv

DATA_TYPE_CHOICES = (
    ('NUMERIC', 'numeric'),
    ('PERCENT','percent'),
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

class CustomDimensionYName(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
        
class CustomDimensionXName(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
        
############# School #####################        

class SchoolDisplayData(models.Model):
    school_indicator = models.ForeignKey("SchoolIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionFor")
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.school_indicator, self.display)

class SchoolDisplayDataY(models.Model):
    school_indicator = models.ForeignKey("SchoolIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionName", blank=True, null=True)
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
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    @property
    def displaydata_x(self):
        index = SchoolDisplayData.objects.filter(school_indicator=self.school_indicator).values_list('display__name',flat=True).order_by("order")
        return index

    @property
    def displaydata_y(self):
        index = SchoolDisplayDataY.objects.filter(school_indicator=self.school_indicator).values_list('display__name',flat=True).order_by("order")
        return index
        #index = SchoolDisplayData.objects.filter(school_indicator=self.school_indicator).values_list('display__name',flat=True).order_by("order")
        #data = SchoolIndicatorData.objects.filter(school_indicator_dataset=self, dimension_x__in=index)
        #result = []

        #y_names = data.values("dimension_y").annotate(Count("dimension_y"))
        #return [i["dimension_y"]  for i in y_names]

    @property
    def get_objects(self, dimension_x, dimension_y):
        try:
           return SchoolIndicatorData.objects.get(school_indicator_dataset=self, dimension_x=dimension_x, dimension_y=dimension_y)
        except:
           return None

    @property
    def displaydata(self):
        dim_x = self.displaydata_x
        dim_y = self.displaydata_y
        result = []
        for y in dim_y:
            data = []
            for x in dim_x:
                try:
                   data.append(SchoolIndicatorData.objects.get(school_indicator_dataset=self, dimension_x=x, dimension_y=y))
                except:
                   data.append(None)
            result.append({"dimension_y":y, "data":data})
        return result
        
    @property
    def data(self):
        return SchoolIndicatorData.objects.filter(school_indicator_dataset=self)
        
    
    def save(self, *args, **kwargs):
        if self.import_file == True:
            super(SchoolIndicatorDataSet, self).save(*args, **kwargs)
            from dataimport.models import DimensionFor, DimensionName
            self.csv_file.file.open(mode='rb')
            reader = csv.reader(self.csv_file.file)
            headers = reader.next()
            
            for row in reader:
                dimension_y = ""
                dimension_x = ""
                for header_index in xrange(len(headers)):
                    if header_index == 0:
                        dim_x, created_x = DimensionFor.objects.get_or_create(name = row[header_index])
                        dimension_x = row[header_index]
                    else:
                        dim_y, created_y = DimensionName.objects.get_or_create(name = headers[header_index])
                        dimension_y = headers[header_index]
                        value = row[header_index]
                        data, created = SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=self,
                                                                    dimension_y=dimension_y,
                                                                    dimension_x=dimension_x)
                        data.key_value = value
                        data.data_type = self.data_type
                        data.save()
                        print "%s - %s [%s]"%(headers[header_index], row[header_index],value)
            
            
            self.import_file = False
        
        return super(SchoolIndicatorDataSet, self).save(*args, **kwargs)
    
    
    
    def __unicode__(self):
        return "%s - %s"%(self.school_indicator, self.school_year)

class SchoolIndicator(models.Model):
    school_indicator_set = models.ForeignKey('SchoolIndicatorSet', blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    order = models.IntegerField(default=0)
    short_title = models.CharField(max_length=100,blank=True)
    description = RichTextField(blank=True)
    data_indicator = models.BooleanField(default=True)
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
    slug = models.SlugField(max_length=100, unique=True,db_index=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    #description = models.TextField(blank=True)
    description = RichTextField(blank=True)
    
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

############# District #####################
class DistrictDisplayData(models.Model):
    district_indicator = models.ForeignKey("DistrictIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionFor")
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.district_indicator, self.display)

class DistrictDisplayDataYDetailData(models.Model):
    detail_set = models.ForeignKey("DistrictDisplayDataYDetailSet")
    dimension_y_name = models.ForeignKey("dataimport.DimensionName")
    dimension_x_name = models.ForeignKey("dataimport.DimensionFor")
    new_dimension_y_name = models.ForeignKey("CustomDimensionYName", blank=True, null=True)
    new_dimension_x_name = models.ForeignKey("CustomDimensionXName", blank=True, null=True)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s - %s"%(self.new_dimension_y_name, self.new_dimension_x_name)

class DistrictDisplayDataYDetailSet(models.Model):
    detail = models.ForeignKey("DistrictDisplayDataYDetail", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=1)
    
    @property
    def detail_data(self):
        return DistrictDisplayDataYDetailData.objects.filter(detail_set = self).order_by('order')
    
    
    def __unicode__(self):
        return self.name

class DistrictDisplayDataYDetail(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True,db_index=True)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.name)
        super(DistrictDisplayDataYDetail, self).save(*args, **kwargs)
    
    @property
    def detail_set(self):
        return DistrictDisplayDataYDetailSet.objects.filter(detail=self).order_by('order')

    def __unicode__(self):
        return self.name

class DistrictDisplayDataY(models.Model):
    district_indicator = models.ForeignKey("DistrictIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionName", blank=True, null=True)
    order = models.IntegerField(default=1)
    detail = models.ForeignKey("DistrictDisplayDataYDetail", blank=True, null=True)
    
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
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after

    @property
    def displaydata_x(self):
        index = DistrictDisplayData.objects.filter(district_indicator=self.district_indicator).values_list('display__name',flat=True).order_by("order")
        return index

    @property
    def displaydata_y(self):
        index = DistrictDisplayDataY.objects.filter(district_indicator=self.district_indicator).values_list('display__name',flat=True).order_by("order")
        return index
        #index = DistrictDisplayData.objects.filter(district_indicator=self.district_indicator).values_list('display__name',flat=True).order_by("order")
        #data = DistrictIndicatorData.objects.filter(district_indicator_dataset=self, dimension_x__in=index)
        #result = []

        #y_names = data.values("dimension_y").annotate(Count("dimension_y"))
        #return [i["dimension_y"]  for i in y_names]

    @property
    def have_detail(self):
        for i in DistrictDisplayDataY.objects.filter(district_indicator=self.district_indicator):
            print i
            if i.detail != None:
                return True
    
    def get_objects(self, dimension_x, dimension_y):
        try:
           return DistrictIndicatorData.objects.get(district_indicator_dataset=self, dimension_x=dimension_x, dimension_y=dimension_y)
        except:
           return None

    @property
    def displaydata(self):
        dim_x = self.displaydata_x
        dim_y = self.displaydata_y
        result = []
        for y in dim_y:
            data = []
            for x in dim_x:
                try:
                   data.append(DistrictIndicatorData.objects.get(district_indicator_dataset=self, dimension_x=x, dimension_y=y))
                except:
                   data.append(None)
            result.append({"dimension_y":DistrictDisplayDataY.objects.get(display__name=y, district_indicator=self.district_indicator),"data":data})
        return result

    @property
    def data(self):
        return DistrictIndicatorData.objects.filter(district_indicator_dataset=self)
    
    def save(self, *args, **kwargs):
        if self.import_file == True:
            super(DistrictIndicatorDataSet, self).save(*args, **kwargs)
            from dataimport.models import DimensionFor, DimensionName
            self.csv_file.file.open(mode='rb')
            reader = csv.reader(self.csv_file.file)
            headers = reader.next()
            
            for row in reader:
                dimension_y = ""
                dimension_x = ""
                for header_index in xrange(len(headers)):
                    if header_index == 0:
                        dim_x, created_x = DimensionFor.objects.get_or_create(name = row[header_index])
                        dimension_x = row[header_index]
                    else:
                        dim_y, created_y = DimensionName.objects.get_or_create(name = headers[header_index])
                        dimension_y = headers[header_index]
                        value = row[header_index]
                        data, created = DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=self,
                                                                    dimension_y=dimension_y,
                                                                    dimension_x=dimension_x)
                        data.key_value = value
                        data.data_type = self.data_type
                        data.save()
                        print "%s - %s [%s]"%(headers[header_index], row[header_index],value)
            
            
            self.import_file = False
        
        return super(DistrictIndicatorDataSet, self).save(*args, **kwargs)
        
    
    
    def __unicode__(self):
        return "%s - %s"%(self.district_indicator, self.school_year)
'''
class DistrictIndicatorCustomIndex(models.Model):
    district_indicator = models.ForeignKey("DistrictIndicator", blank=True, null=True)
    district_indicator_custom_display_set = models.ForeignKey("DistrictIndicatorCustomDisplaySet", blank=True, null=True)

    def __unicode__(self):
        return "%s - %s "%(self.district_indicator.title.title, self.district_indicator_custom_display.name)

class DistrictIndicatorCustomDisplaySet(models.Model):
    district_indicator = models.ManyToManyField("DistrictIndicatorCustomIndex", blank=True, null=True)
    name = models.CharField(max_length=100,blank=True)
    
    def __unicode__(self):
        return "[Custom Display] %s"%self.name

class DistrictIndicatorCustomDisplayCalculateField(models.Model):
    

class DistrictIndicatorCustomDisplayData(models.Model):
    district_indicator_custom_display_set = models.ForeignKey("DistrictIndicatorCustomDisplaySet", blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    calculate_value = models.ForeignKey("DistrictIndicatorCustomDisplaySet", blank=True, null=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)

    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.calculate_value)
'''
class DistrictIndicator(models.Model):
    district_indicator_set = models.ForeignKey('DistrictIndicatorSet', blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    order = models.IntegerField(default=0)
    short_title = models.CharField(max_length=100,blank=True)
    description = RichTextField(blank=True)
    data_indicator = models.BooleanField(default=True)
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
    
    us_state = models.ForeignKey("State", blank=True, null=True)
    district_name = models.CharField(max_length=100)
    district_code = models.CharField(max_length=100,unique=True)
    activate = models.BooleanField(default=True)
    number_of_student = models.IntegerField(blank=True, null=True)
    number_of_teacher = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(max_length=100, unique=True,db_index=True)
    superintendent = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    #description = models.TextField(blank=True)
    description = RichTextField(blank=True)
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

        
############# State #####################

class StateDisplayData(models.Model):
    state_indicator = models.ForeignKey("StateIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionFor")
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.state_indicator, self.display)

class StateDisplayDataY(models.Model):
    state_indicator = models.ForeignKey("StateIndicator", blank=True, null=True)
    display = models.ForeignKey("dataimport.DimensionName", blank=True, null=True)
    order = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s - %s"% (self.state_indicator, self.display)

class StateIndicatorData(models.Model):
    state_indicator_dataset = models.ForeignKey("StateIndicatorDataSet", blank=True, null=True)
    dimension_x = models.CharField(max_length=100, blank=True)
    dimension_y = models.CharField(max_length=100, blank=True)
    key_value = models.CharField(max_length=100, db_index=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_job = models.ForeignKey('dataimport.IndicatorFile', blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.dimension_y, self.dimension_x, self.key_value)

class StateIndicatorDataSet(models.Model):
    state_indicator = models.ForeignKey("StateIndicator", blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear)
    csv_file = models.FileField(upload_to="State_Indicator_Data", blank=True, null=True)
    data_type = models.CharField(max_length=7,choices=DATA_TYPE_CHOICES)
    import_file = models.BooleanField(default=False) #If True start import file, then mark False after
    
    @property
    def displaydata_x(self):
        index = StateDisplayData.objects.filter(state_indicator=self.state_indicator).values_list('display__name',flat=True).order_by("order")
        return index

    @property
    def displaydata_y(self):
        index = StateDisplayDataY.objects.filter(state_indicator=self.state_indicator).values_list('display__name',flat=True).order_by("order")
        return index

        #index = StateDisplayData.objects.filter(state_indicator=self.state_indicator).values_list('display__name',flat=True).order_by("order")
        #data = StateIndicatorData.objects.filter(state_indicator_dataset=self, dimension_x__in=index)
        #result = []

        #y_names = data.values("dimension_y").annotate(Count("dimension_y"))
        #return [i["dimension_y"]  for i in y_names]

    @property
    def get_objects(self, dimension_x, dimension_y):
        try:
           return StateIndicatorData.objects.get(state_indicator_dataset=self, dimension_x=dimension_x, dimension_y=dimension_y)
        except:
           return None

    @property
    def displaydata(self):
        dim_x = self.displaydata_x
        dim_y = self.displaydata_y
        result = []
        for y in dim_y:
            data = []
            for x in dim_x:
                try:
                   data.append(StateIndicatorData.objects.get(state_indicator_dataset=self, dimension_x=x, dimension_y=y))
                except:
                   data.append(None)
            result.append({"dimension_y":y, "data":data})
        return result
        
    @property
    def data(self):
        return StateIndicatorData.objects.filter(state_indicator_dataset=self)
    
    def save(self, *args, **kwargs):
        if self.import_file == True:
            super(StateIndicatorDataSet, self).save(*args, **kwargs)
            from dataimport.models import DimensionFor, DimensionName
            self.csv_file.file.open(mode='rb')
            reader = csv.reader(self.csv_file.file)
            headers = reader.next()
            
            for row in reader:
                dimension_y = ""
                dimension_x = ""
                for header_index in xrange(len(headers)):
                    if header_index == 0:
                        dim_x, created_x = DimensionFor.objects.get_or_create(name = row[header_index])
                        dimension_x = row[header_index]
                    else:
                        dim_y, created_y = DimensionName.objects.get_or_create(name = headers[header_index])
                        dimension_y = headers[header_index]
                        value = row[header_index]
                        data, created = StateIndicatorData.objects.get_or_create(state_indicator_dataset=self,
                                                                    dimension_y=dimension_y,
                                                                    dimension_x=dimension_x)
                        data.key_value = value
                        data.data_type = self.data_type
                        data.save()
                        print "%s - %s [%s]"%(headers[header_index], row[header_index],value)
            
            
            self.import_file = False
        
        return super(StateIndicatorDataSet, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.state_indicator, self.school_year)


class StateIndicator(models.Model):
    state_indicator_set = models.ForeignKey('StateIndicatorSet', blank=True, null=True)
    title = models.ForeignKey(IndicatorTitle)
    order = models.IntegerField(default=0)
    short_title = models.CharField(max_length=100,blank=True)
    description = RichTextField(blank=True)
    data_indicator = models.BooleanField(default=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True)

    @property
    def dataset(self):
        return StateIndicatorDataSet.objects.filter(state_indicator=self).order_by("-school_year__school_year")

    @property
    def displaydata(self):
        return StateDisplayData.objects.filter(state_indicator=self).order_by("order")

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.state_indicator_set.state.indicator_modified = timezone.now()
        self.state_indicator_set.state.save()
        return super(StateIndicator, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s - %s"% (self.state_indicator_set, self.title)


class StateIndicatorSet(models.Model):
    state = models.ForeignKey("State")
    title = models.CharField(max_length=100,blank=False)
    order = models.IntegerField(default=1)

    @property
    def indicators(self):
        return StateIndicator.objects.filter(state_indicator_set=self).order_by("order")
        
        
    def __unicode__(self):
        return "%s - %s"% (self.state.state_name, self.title)
        
class State(models.Model):
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    default_state = models.BooleanField(default=False)
    activate = models.BooleanField(default=True)
    number_of_student = models.IntegerField(blank=True, null=True)
    number_of_teacher = models.IntegerField(blank=True, null=True)
    number_of_school = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True,db_index=True)
    commissioner = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    #description = models.TextField(blank=True)
    description = RichTextField(blank=True)
    indicator_modified = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.state_name)
        super(State, self).save(*args, **kwargs)
    
    @property
    def indicatorset(self):
        return StateIndicatorSet.objects.filter(state=self).order_by("order")
    
    @property
    def districts(self):
        return District.objects.filter(state=self, activate=True).order_by("district_name")
    
    def __unicode__(self):
        return "%s (State)"% self.state_name
        
        
        
        
