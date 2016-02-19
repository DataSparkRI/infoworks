from __future__ import unicode_literals

from django.db import models
import csv

# Create your models here.
class DistrictField(models.Model):
    district_file = models.ForeignKey('DistrictFile')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required) Select district_code, district_name, address, city, state, zip, phone, web_site, superintendent',
                   choices=(('DISTRICT_CODE', 'district_code'),
                            ('DISTRICT_NAME', 'district_name'),
                            ('ADDRESS', 'address'),
                            ('CITY', 'city'),
                            ('STATE', 'state'),
                            ('ZIP','zip'),
                            ('PHONE','phone'),
                            ('WEB_SITE','web_site'),
                            ('SUPERINTENDENT','Superintendent'),
                            )
    )
    def save(self, *args, **kwargs):
        if self.name != '':
            super(DistrictField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class DistrictFile(models.Model):
    school_year = models.CharField(max_length=100)
    file = models.FileField(upload_to="District_Information", blank=True, null=True)
    
    def save(self, *args, **kwargs):

        super(DistrictFile, self).save(*args, **kwargs)
        if DistrictField.objects.filter(district_file=self).count() == 0:
            try:
                f = open(self.file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    print i
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
                            ('SCHOOL_CODE', 'school_code'),
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
                            ('HIGH_GRADE','high_grade')
                            )
    )
    def save(self, *args, **kwargs):
        if self.name != '':
            super(SchoolField, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class SchoolFile(models.Model):
    school_year = models.CharField(max_length=100)
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