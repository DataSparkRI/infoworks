from django.contrib import admin
from data.models import IndicatorTitle, District, DistrictIndicatorSet, DistrictIndicator, School, SchoolIndicatorSet, SchoolIndicator, SchoolNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacher


admin.site.register(IndicatorTitle)



class DistrictNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = DistrictNumberOfStudentAndTeacher

class DistrictIndicatorSetInline(admin.TabularInline):
    model = DistrictIndicatorSet

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'activate','slug', 'modified')
    inlines = [DistrictNumberOfStudentAndTeacherInline, DistrictIndicatorSetInline]
admin.site.register(District, DistrictAdmin)
    
class DistrictIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('district', 'title')
admin.site.register(DistrictIndicatorSet, DistrictIndicatorSetAdmin)

class DistrictIndicatorAdmin(admin.ModelAdmin):
    list_display = ('district_indicator_set','title','school_year','created','modified')
admin.site.register(DistrictIndicator, DistrictIndicatorAdmin)

class DistrictNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
    list_display = ('district', 'school_year','student', 'teacher', 'school')
admin.site.register(DistrictNumberOfStudentAndTeacher, DistrictNumberOfStudentAndTeacherAdmin)



class SchoolNumberOfStudentAndTeacherInline(admin.TabularInline):
    model = SchoolNumberOfStudentAndTeacher

class SchoolIndicatorSetInline(admin.TabularInline):
    model = SchoolIndicatorSet

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'activate','slug', 'modified')
admin.site.register(School, SchoolAdmin)

class SchoolIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('school', 'title')
admin.site.register(SchoolIndicatorSet, SchoolIndicatorSetAdmin)

class SchoolIndicatorAdmin(admin.ModelAdmin):
    list_display = ('school_indicator_set','title','school_year','created','modified')
admin.site.register(SchoolIndicator, SchoolIndicatorAdmin)

class SchoolNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
    list_display = ('school', 'school_year','student', 'teacher')
admin.site.register(SchoolNumberOfStudentAndTeacher, SchoolNumberOfStudentAndTeacherAdmin)



# Register your models here.
