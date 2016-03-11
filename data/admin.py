from django.contrib import admin
from data.models import SchoolYear, IndicatorTitle, DetailDataSetTitle, \
District, DistrictDisplayData, DistrictIndicatorDataSet, DistrictIndicatorSet, DistrictIndicator, DistrictDisplayDataY, \
School, SchoolIndicatorSet, SchoolIndicator, SchoolDisplayData, SchoolIndicatorDataSet, SchoolDisplayDataY, \
State, StateIndicatorSet, StateIndicator, StateDisplayData, StateIndicatorDataSet, StateDisplayDataY, \
DistrictIndicatorData, DistrictIndicatorDetailDataSet

from django.contrib import messages

#from data.form import StateDisplayDataYForm, DistrictDisplayDataYForm, SchoolDisplayDataYForm

admin.site.register(IndicatorTitle)

##### state #########
def write_default_state_indicator_set(modeladmin, request, queryset):
    for q in queryset:
        StateIndicatorSet.objects.get_or_create(title='Student Achievement' ,state=q, order=1)
        StateIndicatorSet.objects.get_or_create(title='Teaching' ,state=q, order=2)
        StateIndicatorSet.objects.get_or_create(title='Families and Communities' ,state=q, order=3)
        StateIndicatorSet.objects.get_or_create(title='Safe and Supportive Schools' ,state=q, order=4)
        StateIndicatorSet.objects.get_or_create(title='Funding and Resources' ,state=q, order=5)
        StateIndicatorSet.objects.get_or_create(title='Other' ,state=q, order=6)
    try:
        messages.add_message(request, messages.INFO, "Done")
    except:
        pass

def write_default_state_indicator(modeladmin, request, queryset):
    for q in queryset:
        if q.title == "Student Achievement":
            title, created = IndicatorTitle.objects.get_or_create(title="Accountability")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
            title, created = IndicatorTitle.objects.get_or_create(title="PARCC Assessments")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=2)
            title, created = IndicatorTitle.objects.get_or_create(title="NECAP Assessments")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=3)
            title, created = IndicatorTitle.objects.get_or_create(title="SAT Exams (High School)")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=4)
            title, created = IndicatorTitle.objects.get_or_create(title="AP Exams (High School)")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=5)
            title, created = IndicatorTitle.objects.get_or_create(title="Developmental Reading Assessment")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=6)
            
        elif q.title == "Teaching":
            title, created = IndicatorTitle.objects.get_or_create(title="Qualifications and Teacher-Student Ratio")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
            
        elif q.title == "Families and Communities":
            title, created = IndicatorTitle.objects.get_or_create(title="Student Characteristics")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
        elif q.title == "Safe and Supportive Schools":
            title, created = IndicatorTitle.objects.get_or_create(title="Attendance")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
            title, created = IndicatorTitle.objects.get_or_create(title="Four Year Graduation Rate")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=2)
            title, created = IndicatorTitle.objects.get_or_create(title="Five Year Graduation Rate")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=3)
            title, created = IndicatorTitle.objects.get_or_create(title="Incidents of Suspension")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=4)
            title, created = IndicatorTitle.objects.get_or_create(title="Student Indicators")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=5)

        elif q.title == "Funding and Resources":
            title, created = IndicatorTitle.objects.get_or_create(title="Uniform Chart of Accounts (UCOA)")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
        elif q.title == "Other":
            title, created = IndicatorTitle.objects.get_or_create(title="NAEP Exams")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=1)
            title, created = IndicatorTitle.objects.get_or_create(title="SurveyWorks Reports")
            StateIndicator.objects.get_or_create(state_indicator_set=q, title=title, order=2)
        else:
            pass
    try:
        messages.add_message(request, messages.INFO, "Done")
    except:
        pass

class StateDisplayDataYInline(admin.TabularInline):
    model = StateDisplayDataY
    #form = StateDisplayDataYForm

class StateDisplayDataInline(admin.TabularInline):
    model = StateDisplayData
    
class SchoolDisplayDataInline(admin.TabularInline):
    model = SchoolDisplayData

class StateIndicatorSetInline(admin.TabularInline):
    model = StateIndicatorSet

class StateIndicatorDataSetInline(admin.TabularInline):
    model = StateIndicatorDataSet

class StateIndicatorInline(admin.TabularInline):
    model = StateIndicator

class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'default_state', 'activate','slug', 'indicator_modified')
    inlines = [StateIndicatorSetInline]
    actions = [write_default_state_indicator_set]
admin.site.register(State, StateAdmin)
    
class StateIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('state', 'title')
    search_fields = ['state__state_name','title']
    inlines = [StateIndicatorInline]
    actions = [write_default_state_indicator]
admin.site.register(StateIndicatorSet, StateIndicatorSetAdmin)

class StateIndicatorAdmin(admin.ModelAdmin):
    list_display = ('state_indicator_set','title','created','modified')
    raw_id_fields = ('state_indicator_set',)
    inlines = [StateDisplayDataInline, StateDisplayDataYInline, StateIndicatorDataSetInline]
admin.site.register(StateIndicator, StateIndicatorAdmin)

###### district ########
def write_default_district_indicator_set(modeladmin, request, queryset):
    for q in queryset:
        DistrictIndicatorSet.objects.get_or_create(title='Student Achievement' ,district=q, order=1)
        DistrictIndicatorSet.objects.get_or_create(title='Teaching' ,district=q, order=2)
        DistrictIndicatorSet.objects.get_or_create(title='Families and Communities' ,district=q, order=3)
        DistrictIndicatorSet.objects.get_or_create(title='Safe and Supportive Schools' ,district=q, order=4)
        DistrictIndicatorSet.objects.get_or_create(title='Funding and Resources' ,district=q, order=5)
        DistrictIndicatorSet.objects.get_or_create(title='Other' ,district=q, order=6)
    try:
        messages.add_message(request, messages.INFO, "Done")
    except:
        pass

def write_default_district_indicator(modeladmin, request, queryset):
    for q in queryset:
        if q.title == "Student Achievement":
            title, created = IndicatorTitle.objects.get_or_create(title="Accountability")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
            title, created = IndicatorTitle.objects.get_or_create(title="PARCC Assessments")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=2)
            title, created = IndicatorTitle.objects.get_or_create(title="NECAP Assessments")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=3)
            title, created = IndicatorTitle.objects.get_or_create(title="SAT Exams (High School)")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=4)
            title, created = IndicatorTitle.objects.get_or_create(title="AP Exams (High School)")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=5)
            
        elif q.title == "Teaching":
            title, created = IndicatorTitle.objects.get_or_create(title="Qualifications and Teacher-Student Ratio")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
            
        elif q.title == "Families and Communities":
            title, created = IndicatorTitle.objects.get_or_create(title="Student Characteristics")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
        elif q.title == "Safe and Supportive Schools":
            title, created = IndicatorTitle.objects.get_or_create(title="Attendance")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
            title, created = IndicatorTitle.objects.get_or_create(title="Four Year Graduation Rate")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=2)
            title, created = IndicatorTitle.objects.get_or_create(title="Five Year Graduation Rate")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=3)
            title, created = IndicatorTitle.objects.get_or_create(title="Incidents of Suspension")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=4)
            title, created = IndicatorTitle.objects.get_or_create(title="Student Indicators")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=5)

        elif q.title == "Funding and Resources":
            title, created = IndicatorTitle.objects.get_or_create(title="Uniform Chart of Accounts (UCOA)")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
        elif q.title == "Other":
            title, created = IndicatorTitle.objects.get_or_create(title="SurveyWorks Reports")
            DistrictIndicator.objects.get_or_create(district_indicator_set=q, title=title, order=1)
        else:
            pass
    try:
        messages.add_message(request, messages.INFO, "Done")
    except:
        pass


class DistrictIndicatorDetailDataSetInline(admin.TabularInline):
    model = DistrictIndicatorDetailDataSet

class DistrictDisplayDataYInline(admin.TabularInline):
    model = DistrictDisplayDataY
    #form = DistrictDisplayDataYForm

class DistrictDisplayDataInline(admin.TabularInline):
    model = DistrictDisplayData
    
class SchoolDisplayDataInline(admin.TabularInline):
    model = SchoolDisplayData

class DistrictIndicatorSetInline(admin.TabularInline):
    model = DistrictIndicatorSet

class DistrictIndicatorDataSetInline(admin.TabularInline):
    model = DistrictIndicatorDataSet

class DistrictIndicatorInline(admin.TabularInline):
    model = DistrictIndicator

class DistrictIndicatorDataAdmin(admin.ModelAdmin):
    inlines = [DistrictIndicatorDetailDataSetInline]
admin.site.register(DistrictIndicatorData, DistrictIndicatorDataAdmin)
    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'activate','slug', 'indicator_modified')
    inlines = [DistrictIndicatorSetInline]
    actions = [write_default_district_indicator_set]
admin.site.register(District, DistrictAdmin)
    
class DistrictIndicatorSetAdmin(admin.ModelAdmin):
    list_display = ('district', 'title')
    search_fields = ['district__district_name','title']
    inlines = [DistrictIndicatorInline]
    actions = [write_default_district_indicator]
admin.site.register(DistrictIndicatorSet, DistrictIndicatorSetAdmin)

class DistrictIndicatorAdmin(admin.ModelAdmin):
    list_display = ('district_indicator_set','title','created','modified')
    raw_id_fields = ('district_indicator_set',)
    inlines = [DistrictDisplayDataInline, DistrictDisplayDataYInline, DistrictIndicatorDataSetInline]
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

class SchoolDisplayDataYInline(admin.TabularInline):
    model = SchoolDisplayDataY
    #form = SchoolDisplayDataYForm

class SchoolIndicatorSetInline(admin.TabularInline):
    model = SchoolIndicatorSet

class SchoolIndicatorSetInline(admin.TabularInline):
    model = SchoolIndicatorSet

class SchoolIndicatorDataSetInline(admin.TabularInline):
    model = SchoolIndicatorDataSet

class SchoolIndicatorInline(admin.TabularInline):
    model = SchoolIndicator

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('district','school_name', 'activate','slug', 'indicator_modified')
    inlines = [SchoolIndicatorSetInline]
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
    #form = SchoolDisplayDataYForm
    inlines = [SchoolDisplayDataInline, SchoolDisplayDataYInline, SchoolIndicatorDataSetInline]
admin.site.register(SchoolIndicator, SchoolIndicatorAdmin)
admin.site.register(SchoolYear)
admin.site.register(DetailDataSetTitle)
#class SchoolNumberOfStudentAndTeacherAdmin(admin.ModelAdmin):
#    list_display = ('school', 'school_year','student', 'teacher')
#admin.site.register(SchoolNumberOfStudentAndTeacher, SchoolNumberOfStudentAndTeacherAdmin)



# Register your models here.
