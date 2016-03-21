from django.contrib import admin
from models import Dictionary, Category, Config

# Register your models here.

class DictionaryInLine(admin.TabularInline):
    model = Dictionary

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [DictionaryInLine]

admin.site.register(Category, CategoryAdmin)

class ConfigAdmin(admin.ModelAdmin):
    display = ('name', 'value')
admin.site.register(Config, ConfigAdmin)