from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
# Create your models here.
class Config(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "%s : %s"%(self.name, self.value)

class Category(models.Model):
    category = models.CharField(max_length=100)
    
    @property
    def dictionary(self):
        return Dictionary.objects.filter(category=self)

class Dictionary(models.Model):
    category = models.ForeignKey("Category")
    term = models.CharField(max_length=100)
    content = RichTextField(blank=True)
    
    def __unicode__(self):
        return "%s - %s"% (self.category, self.term)
    
class About(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    active = models.BooleanField(default=True, verbose_name="Active page")
    slug = models.SlugField(max_length=100, unique=True,db_index=True,blank=True,null=True)
    image = models.ImageField(upload_to='about_images', null=True, blank=True)
    image_text = models.TextField(blank=True)
    notes = models.TextField(blank=True,  help_text="This field is for internal use only.")
    content = RichTextField(blank=True)
    order = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.title)
        super(About, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title
    
class New(models.Model):
    about = models.ForeignKey(About, null=True, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    html_text = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title