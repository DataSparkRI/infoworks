from django.contrib import admin
from data.models import DistrictDisplayData, SchoolDisplayData, SchoolYear, DistrictIndicatorDataSet, SchoolIndicatorDataSet, IndicatorTitle, District, DistrictIndicatorSet, DistrictIndicator, School, SchoolIndicatorSet, SchoolIndicator, SchoolNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacher
from django.contrib import messages

admin.site.register(IndicatorTitle)

def write_default_district_indicator_set(modeladmin, request, queryset):
    for q in queryset:
        DistrictIndicatorSet.objects.get_or_create(title='Student Achievement' ,district=q, order=1)
        DistrictIndicatorSet.objects.get_or_create(title='Teaching' ,district=q, order=2)
        DistrictIndicatorSet.objects.get_or_create(title='Families and Communities' ,district=q, order=3)
        DistrictIndicatorSet.objects.get_or_create(title='Safe and Supportive Schools' ,district=q, order=4)
        DistrictIndicatorSet.objects.get_or_create(title='Funding and Resources' ,district=q, order=5)
        DistrictIndicatorSet.objects.get_or_create(title='Other' ,district=q, order=6)
    messages.add_message(request, messages.INFO, "Done")

class DistrictDisplayDataInline(admin.TabularInline):
    model = DistrictDisplayData
    
class SchoolDisplayDataInline(admin.TabularInline):
    model = SchoolDisplayData

class DistrictNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = DistrictNumberOfStudentAndTeacher

class DistrictIndicatorSetInline(admin.TabularInline):
    model = DistrictIndicatorSet

class DistrictIndicatorDataSetInline(admin.TabularInline):
    model = DistrictIndicatorDataSet

class DistrictIndicatorInline(admin.TabularInline):
    model = DistrictIndicator

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'activate','slug', 'indicator_modified')
    inlines = [DistrictNumberOfStudentAndTeacherInline, DistrictIndicatorSetInline]
    actions = [write_default_district_indicator_set]
admin.site.register(District, DistrictAdmin)
    
class DistrictIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('district', 'title')
    search_fields = ['district__district_name','title']
    inlines = [DistrictIndicatorInline]
admin.site.register(DistrictIndicatorSet, DistrictIndicatorSetAdmin)

class DistrictIndicatorAdmin(admin.ModelAdmin):
    list_display = ('district_indicator_set','title','created','modified')
    raw_id_fields = ('district_indicator_set',)
    inlines = [DistrictDisplayDataInline, DistrictIndicatorDataSetInline]
admin.site.register(DistrictIndicator, DistrictIndicatorAdmin)

#class DistrictNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
#    list_display = ('district', 'school_year','student', 'teacher', 'school')
#admin.site.register(DistrictNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacherAdmin)


def write_default_school_indicator_set(modeladmin, request, queryset):
    for q in queryset:
        SchoolIndicatorSet.objects.get_or_create(title='Student Achievement' ,school=q, order=1)
        SchoolIndicatorSet.objects.get_or_create(title='Teaching' ,school=q, order=2)
        SchoolIndicatorSet.objects.get_or_create(title='Families and Communities' ,school=q, order=3)
        SchoolIndicatorSet.objects.get_or_create(title='Safe and Supportive Schools' ,school=q, order=4)
        SchoolIndicatorSet.objects.get_or_create(title='Funding and Resources' ,school=q, order=5)
        SchoolIndicatorSet.objects.get_or_create(title='Other' ,school=q, order=6)
    messages.add_message(request, messages.INFO, "Done")


class SchoolNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = SchoolNumberOfStudentAndTeacher

class SchoolIndicatorSetInline(admin.TabularInline):
    model = SchoolIndicatorSet


class SchoolNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = SchoolNumberOfStudentAndTeacher

class SchoolIndicatorSetInline(admin.TabularInline):
    model = SchoolIndicatorSet

class SchoolIndicatorDataSetInline(admin.TabularInline):
    model = SchoolIndicatorDataSet

class SchoolIndicatorInline(admin.TabularInline):
    model = SchoolIndicator

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('district','school_name', 'activate','slug', 'indicator_modified')
    inlines = [SchoolNumberOfStudentAndTeacherInline, SchoolIndicatorSetInline]
    actions = [write_default_school_indicator_set]
admin.site.register(School, SchoolAdmin)

class SchoolIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('school', 'title')
    search_fields = ['school__school_name','title']
    inlines = [SchoolIndicatorInline]
admin.site.register(SchoolIndicatorSet, SchoolIndicatorSetAdmin)

class SchoolIndicatorAdmin(admin.ModelAdmin):
    list_display = ('school_indicator_set','title','created','modified')
    raw_id_fields = ('school_indicator_set',)
    inlines = [SchoolDisplayDataInline, SchoolIndicatorDataSetInline]
admin.site.register(SchoolIndicator, SchoolIndicatorAdmin)
admin.site.register(SchoolYear)
#class SchoolNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
#    list_display = ('school', 'school_year','student', 'teacher')
#admin.site.register(SchoolNumberOfStudentAndTeacher, SchoolNumberOfStudentAndTeacherAdmin)



# Register your models here.
