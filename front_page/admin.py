from django.contrib import admin
from models import Dictionary, Category

# Register your models here.

class DictionaryInLine(admin.TabularInline):
    model = Dictionary

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    inlines = [DictionaryInLine]

admin.site.register(Category, CategoryAdmin)
