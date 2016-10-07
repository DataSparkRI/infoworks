from django.contrib import admin
from models import Dictionary, Category, Config, About, New

# Register your models here.

class DictionaryInLine(admin.TabularInline):
    model = Dictionary

class NewInLine(admin.TabularInline):
    model = New

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [DictionaryInLine]
admin.site.register(Category, CategoryAdmin)

class ConfigAdmin(admin.ModelAdmin):
    display = ('name', 'value')
admin.site.register(Config, ConfigAdmin)

class AboutAdmin(admin.ModelAdmin):
    display = ('title','subtitle','order')
    inlines = [NewInLine]
admin.site.register(About, AboutAdmin)