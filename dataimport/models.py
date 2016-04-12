from __future__ import unicode_literals

from django.db import models
import csv
from data.models import StateIndicator, DistrictIndicator, SchoolIndicator, IndicatorTitle, SchoolYear

# Create your models here.
class SystemCode(models.Model):
    code = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    
    def __unicode__(self):
        return "%s - %s"%(self.code, self.display_name)

class LookUpTableElement(models.Model):
    table = models.ForeignKey('LookUpTable')
    file_code = models.CharField(max_length=100, blank=True)
    system_code = models.ForeignKey('SystemCode')
    
    def __unicode__(self):
        return "%s - %s"%(self.file_code, self.system_code)

class LookUpTable(models.Model):
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    
    def get_code(self, file_code):
        try:
            return LookUpTableElement.objects.get(table=self, file_code=file_code).system_code.code
        except:
            return file_code
    
    @property
    def elements(self):
        return LookUpTableElement.objects.filter(table=self).order_by("system_code")
    
    def __unicode__(self):
        return self.name


class StateField(models.Model):
    state_file = models.ForeignKey('StateFile')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required) Select state_code, state_name, address, city, state, zip, phone, web_site, commissioner',
                   choices=(('STATE_CODE', 'state_code'),
                            ('STATE_NAME', 'state_name'),
                            ('ADDRESS', 'address'),
                            ('CITY', 'city'),
                            ('STATE', 'state'),
                            ('ZIP','zip'),
                            ('PHONE','phone'),
                            ('WEB_SITE','web_site'),
                            ('COMMISSIONER','Commissioner'),
                            ('DESCRIPTION','Description'),
                            ('NUMBER_STUDENT','number of student'),
                            ('NUMBER_TEACHER','number of teacher'),
                            ('NUMBER_SCHOOL','number of school'),
                            )
    )
    def save(self, *args, **kwargs):
        if self.name != '':
            super(StateField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class StateFile(models.Model):
    school_year = models.ForeignKey(SchoolYear)
    file = models.FileField(upload_to="State_Information", blank=True, null=True)
    
    def save(self, *args, **kwargs):

        super(StateFile, self).save(*args, **kwargs)
        if StateField.objects.filter(state_file=self).count() == 0:
            try:
                f = open(self.file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    try:
                       StateField.objects.get_or_create(state_file=self, name=i)
                    except:
                       pass
            except IOError:
                pass
    
    def __unicode__(self):
        return "%s"% self.school_year


class DistrictField(models.Model):
    district_file = models.ForeignKey('DistrictFile')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required) Select district_code, district_name, address, city, state, zip, phone, web_site, superintendent',
                   choices=(('STATE_CODE', 'state_code'),
                            ('DISTRICT_CODE', 'district_code (required)'),
                            ('DISTRICT_NAME', 'district_name'),
                            ('ADDRESS', 'address'),
                            ('CITY', 'city'),
                            ('STATE', 'state'),
                            ('ZIP','zip'),
                            ('PHONE','phone'),
                            ('WEB_SITE','web_site'),
                            ('SUPERINTENDENT','Superintendent'),
                            ('DESCRIPTION','Description'),
                            ('NUMBER_STUDENT','number of student'),
                            ('NUMBER_TEACHER','number of teacher')
                            )
    )
    def save(self, *args, **kwargs):
        if self.name != '':
            super(DistrictField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class DistrictFile(models.Model):
    school_year = models.ForeignKey(SchoolYear)
    file = models.FileField(upload_to="District_Information", blank=True, null=True)
    
    def save(self, *args, **kwargs):

        super(DistrictFile, self).save(*args, **kwargs)
        if DistrictField.objects.filter(district_file=self).count() == 0:
            try:
                f = open(self.file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    try:
                       DistrictField.objects.get_or_create(district_file=self, name=i)
                    except:
                       pass
            except IOError:
                pass
    
    def __unicode__(self):
        return "%s"% self.school_year
        
class SchoolField(models.Model):
    school_file = models.ForeignKey('SchoolFile')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required) [low_grade and high_grade only accept PK, K, and 1 - 12] [grade_type only accept "Emh"]',
                   choices=(('DISTRICT_CODE', 'district_code'),
                            ('PRINCIPAL', 'principal'),
                            ('SCHOOL_CODE', 'school_code (required)'),
                            ('SCHOOL_NAME', 'school_name'),
                            ('SCHOOL_TYPE', 'school_type'),
                            ('GRADE_TYPE', 'grade_type'),
                            ('ADDRESS', 'address'),
                            ('CITY', 'city'),
                            ('STATE', 'state'),
                            ('ZIP','zip'),
                            ('PHONE','phone'),
                            ('WEB_SITE','web_site'),
                            ('LOW_GRADE', 'low_grade'),
                            ('HIGH_GRADE','high_grade'),
                            ('DESCRIPTION','Description'),
                            ('NUMBER_STUDENT','number of student'),
                            ('NUMBER_TEACHER','number of teacher')
                            )
    )
    def save(self, *args, **kwargs):
        if self.name != '':
            super(SchoolField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class SchoolFile(models.Model):
    school_year = models.ForeignKey(SchoolYear)
    file = models.FileField(upload_to="School_Information", blank=True, null=True)
    
    def save(self, *args, **kwargs):

        super(SchoolFile, self).save(*args, **kwargs)
        if SchoolField.objects.filter(school_file=self).count() == 0:
            try:
                f = open(self.file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    try:
                       SchoolField.objects.get_or_create(school_file=self, name=i)
                    except:
                       pass
            except:
                pass
    
    def __unicode__(self):
        return "%s"% self.school_year

class DimensionName(models.Model):
    name = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.name
        
class DimensionFor(models.Model):
    name = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name
    
class IndicatorField(models.Model):
    indicator_file = models.ForeignKey('IndicatorFile')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required)',
                   choices=(
                            ('SCHOOL_YEAR', 'school_year'),
                            ('STATE_CODE', 'state_code (required pick one)'),
                            ('DISTRICT_CODE', 'district_code (required pick one)'),
                            ('SCHOOL_CODE', 'school_code (required pick one)'),
                            ('DIMENSION', 'dimension'),
                            ('01_ADD_ON', '1. add on "[data]"'),
                            ('02_ADD_ON_WITH_HEADER', '1. add on with header "[header] [data]"'),
                            ('03_ADD_ON', '2. add on "[data]"'),
                            ('04_ADD_ON_WITH_HEADER', '2. add on with header "[header] [data]"'),
                            ('05_ADD_ON', '3. add on "[data]"'),
                            ('06_ADD_ON_WITH_HEADER', '3. add on with header "[header] [data]"'),
                            ('07_ADD_ON', '4. add on "[data]"'),
                            ('08_ADD_ON_WITH_HEADER', '4. add on with header "[header] [data]"'),
                            ('09_ADD_ON', '5. add on "[data]"'),
                            ('10_ADD_ON_WITH_HEADER', '5. add on with header "[header] [data]"'),
                            ))
    data_type = models.CharField(max_length=30, blank=True, null=True,
                    help_text='(required)',
                    choices=(('NUMERIC', 'numeric'),
                            ('PERCENT','percent'),
                            ('STRING', 'string'),
                            ))
    dimension_name = models.ForeignKey('DimensionName', blank=True, null=True)
    lookup_table = models.ForeignKey('LookUpTable', blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.name != '':
            super(IndicatorField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class IndicatorFile(models.Model):
    name = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear, blank=True, null=True)
    file = models.FileField(upload_to="Indicator_Information", blank=True, null=True)
    state_indicator = models.BooleanField(default=False)
    district_indicator = models.BooleanField(default=False)
    school_indicator = models.BooleanField(default=False)
    indicator = models.ForeignKey(IndicatorTitle, blank=True, null=True)
    indicator_for = models.ForeignKey(DimensionFor, blank=True, null=True)
    def save(self, *args, **kwargs): 

        super(IndicatorFile, self).save(*args, **kwargs)
        if IndicatorField.objects.filter(indicator_file=self).count() == 0:
            try:
                f = open(self.file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    try:
                       IndicatorField.objects.get_or_create(indicator_file=self, name=i)
                    except:
                       pass
            except:
                pass
    
    def __unicode__(self):
        return "%s - %s - %s"% (self.name, self.indicator, self.indicator_for)
        
        
class IndicatorDetailFile(models.Model):
    name = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear)
    file = models.FileField(upload_to="Indicator_Detail_Information", blank=True, null=True)
    state_indicator = models.BooleanField(default=False)
    district_indicator = models.BooleanField(default=False)
    school_indicator = models.BooleanField(default=False)
    #indicator = models.ForeignKey(IndicatorTitle, blank=True, null=True)
    #indicator_for = models.ForeignKey(DimensionFor, blank=True, null=True)
    #def save(self, *args, **kwargs): 

    #    super(IndicatorFile, self).save(*args, **kwargs)
    #    if IndicatorField.objects.filter(indicator_file=self).count() == 0:
    #        try:
    #            f = open(self.file.path, 'rb')
    #            reader = csv.reader(f)
    #            headers = reader.next()
    #            for i in headers:
    #                try:
    #                   IndicatorField.objects.get_or_create(indicator_file=self, name=i)
    #                except:
    #                   pass
    #        except:
    #            pass
    
    def __unicode__(self):
        return "%s - %s"% (self.name, self.school_year)
