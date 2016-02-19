from django.contrib import admin
from data.models import DistrictIndicatorDataSet, SchoolIndicatorDataSet, IndicatorTitle, District, DistrictIndicatorSet, DistrictIndicator, School, SchoolIndicatorSet, SchoolIndicator, SchoolNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacher


admin.site.register(IndicatorTitle)



class DistrictNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = DistrictNumberOfStudentAndTeacher

class DistrictIndicatorSetInline(admin.TabularInline):
    model = DistrictIndicatorSet

class DistrictIndicatorDataSetInline(admin.TabularInline):
    model = DistrictIndicatorDataSet

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'activate','slug', 'indicator_modified')
    inlines = [DistrictNumberOfStudentAndTeacherInline, DistrictIndicatorSetInline]
admin.site.register(District, DistrictAdmin)
    
class DistrictIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('district', 'title')
    search_fields = ['district__district_name','title']
admin.site.register(DistrictIndicatorSet, DistrictIndicatorSetAdmin)

class DistrictIndicatorAdmin(admin.ModelAdmin):
    list_display = ('district_indicator_set','title','created','modified')
    raw_id_fields = ('district_indicator_set',)
    inlines = [DistrictIndicatorDataSetInline]
admin.site.register(DistrictIndicator, DistrictIndicatorAdmin)

#class DistrictNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
#    list_display = ('district', 'school_year','student', 'teacher', 'school')
#admin.site.register(DistrictNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacherAdmin)


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

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('district','school_name', 'activate','slug', 'indicator_modified')
    inlines = [SchoolNumberOfStudentAndTeacherInline, SchoolIndicatorSetInline]
admin.site.register(School, SchoolAdmin)

class SchoolIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('school', 'title')
    search_fields = ['school__school_name','title']
admin.site.register(SchoolIndicatorSet, SchoolIndicatorSetAdmin)

class SchoolIndicatorAdmin(admin.ModelAdmin):
    list_display = ('school_indicator_set','title','created','modified')
    raw_id_fields = ('school_indicator_set',)
    inlines = [SchoolIndicatorDataSetInline]
admin.site.register(SchoolIndicator, SchoolIndicatorAdmin)

#class SchoolNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
#    list_display = ('school', 'school_year','student', 'teacher')
#admin.site.register(SchoolNumberOfStudentAndTeacher, SchoolNumberOfStudentAndTeacherAdmin)



# Register your models here.
