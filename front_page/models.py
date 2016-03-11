from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
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
    