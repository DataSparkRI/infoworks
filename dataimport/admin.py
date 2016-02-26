from django.contrib import admin
from dataimport.models import DimensionFor, DistrictFile, DistrictField, SchoolFile, SchoolField, IndicatorFile, IndicatorField, DimensionName
from data.models import District, School
from dataimport.actions.ImportIndicator import import_indicator
import csv
from django.contrib import messages
# Register your models here.
def get_or_none(objects, match_option):
    try:
        return objects.get(match_option=match_option).name
    except:
        print match_option
        return None

def get_index_or_none(headers, option):
    try:
        return headers.index(option)
    except:
        return None

def import_or_update_district_information(modeladmin, request, queryset):
    for q in queryset:
        path = q.file.path
        fields = DistrictField.objects.filter(district_file=q)
    
        district_code = get_or_none(fields, "DISTRICT_CODE")
        district_name = get_or_none(fields, "DISTRICT_NAME")
        address = get_or_none(fields, "ADDRESS")
        city = get_or_none(fields, "CITY")
        state = get_or_none(fields, "STATE")
        zip = get_or_none(fields, "ZIP")
        phone = get_or_none(fields, "PHONE")
        web_site = get_or_none(fields, "WEB_SITE")
        superintendent = get_or_none(fields, "SUPERINTENDENT")
        description = get_or_none(fields, "DESCRIPTION")

        with open(path) as f:
            reader = csv.reader(f)
            headers = reader.next()
            
            district_code_index = get_index_or_none(headers, district_code)
            district_name_index = get_index_or_none(headers, district_name)
            address_index = get_index_or_none(headers, address)
            city_index = get_index_or_none(headers, city)
            state_index = get_index_or_none(headers, state)
            zip_index = get_index_or_none(headers, zip)
            phone_index = get_index_or_none(headers, phone)
            web_site_index = get_index_or_none(headers, web_site)
            superintendent_index = get_index_or_none(headers, superintendent)
            description_index = get_index_or_none(headers, description)
            
            for row in reader:
                district, created = District.objects.get_or_create(
                    district_code=row[district_code_index]
                    )
                
                if district_name_index != None:
                    district.district_name = row[district_name_index]
                #district.slug = row[district_code_index].lower()
                if address_index != None:
                    district.street = row[address_index]
                if city_index != None:
                    district.city = row[city_index]
                if state_index != None:
                    district.state = row[state_index]
                if zip_index != None:
                    district.zip = row[zip_index]
                if phone_index != None:
                    district.phone = row[phone_index]
                if web_site_index != None:
                    district.website = row[web_site_index]
                if superintendent_index != None:
                    district.superintendent = row[superintendent_index]
                if description_index != None:
                    district.description = row[description_index]
                    
                district.save()

    messages.add_message(request, messages.INFO, "Done")


class DistrictFieldInline(admin.TabularInline):
    model = DistrictField

class DistrictFileAdmin(admin.ModelAdmin):
    inlines = [DistrictFieldInline]
    actions = [import_or_update_district_information]
admin.site.register(DistrictFile, DistrictFileAdmin)

def import_or_update_school_information(modeladmin, request, queryset):
    for q in queryset:
        path = q.file.path
        fields = SchoolField.objects.filter(school_file=q)
        
        district_code = get_or_none(fields, "DISTRICT_CODE")
        school_code = get_or_none(fields,"SCHOOL_CODE")
        school_name = get_or_none(fields,"SCHOOL_NAME")
        school_type = get_or_none(fields,"SCHOOL_TYPE")
        grade_type = get_or_none(fields,"GRADE_TYPE")
        
        address = get_or_none(fields,"ADDRESS")
        city = get_or_none(fields,"CITY")
        state = get_or_none(fields,"STATE")
        zip = get_or_none(fields,"ZIP")
        phone = get_or_none(fields,"PHONE")
        web_site = get_or_none(fields,"WEB_SITE")
        low_grade = get_or_none(fields,"LOW_GRADE")
        high_grade = get_or_none(fields,"HIGH_GRADE")
        principal = get_or_none(fields,"PRINCIPAL")
        description = get_or_none(fields, "DESCRIPTION")

        with open(path) as f:
            reader = csv.reader(f)
            headers = reader.next()
            
            district_code_index = get_index_or_none(headers, district_code)
            school_code_index = get_index_or_none(headers,school_code)
            school_name_index = get_index_or_none(headers,school_name)
            school_type_index = get_index_or_none(headers,school_type)
            grade_type_index = get_index_or_none(headers,grade_type)
            
            address_index = get_index_or_none(headers,address)
            city_index = get_index_or_none(headers,city)
            state_index = get_index_or_none(headers,state)
            zip_index = get_index_or_none(headers,zip)
            phone_index = get_index_or_none(headers,phone)
            web_site_index = get_index_or_none(headers,web_site)
            low_grade_index = get_index_or_none(headers,low_grade)
            high_grade_index = get_index_or_none(headers,high_grade)
            
            principal_index = get_index_or_none(headers,principal)
            description_index = get_index_or_none(headers, description)

            for row in reader:
                school, created = School.objects.get_or_create(
                    school_code=row[school_code_index]
                    )
                if school_code_index != None:    
                    school.school_name = row[school_name_index]
                #school.slug = row[school_code_index].lower()
                if school_type_index != None:
                    school.school_type = row[school_type_index]
                if address_index != None:
                    school.street = row[address_index]
                if city_index != None:
                    school.city = row[city_index]
                if state_index != None:
                    school.state = row[state_index]
                if zip_index != None:
                    school.zip = row[zip_index]
                if phone_index != None:
                    school.phone = row[phone_index]
                if web_site_index != None:
                    school.website = row[web_site_index]
                if principal_index != None:
                    school.principal = row[principal_index]
                if description_index != None:
                    school.description = row[description_index]
                
                if district_code_index != None:
                    school.district = District.objects.get(district_code = row[district_code_index])
                if grade_type_index != None:
                    school.grade_type = row[grade_type_index]
                
                    if row[grade_type_index][0].isupper():
                        school.elementary_school = True
                    if row[grade_type_index][1].isupper():
                        school.middle_school = True
                    if row[grade_type_index][2].isupper():
                        school.high_school = True

                
                if low_grade_index != None and high_grade_index != None:
                    grade = ({"id":'pk'}, {"id":'k'}, {"id":'1'}, {"id":'2'},{"id":'3'},
                            {"id":'4'},{"id":'5'},{"id":'6'},
                            {"id":'7'},{"id":'8'},
                            {"id":'9'},{"id":'10'},
                            {"id":'11'},{"id":'12'})
                    lock = False
                    for i in grade:
                        if row[low_grade_index].lower() == i['id']:
                            lock = True
                        if lock:
                            setattr(school, 'grade_'+i['id'], True)
                        if row[high_grade_index].lower() == i['id']:
                            lock = False
                            break
                print school.grade_pk
                            
                school.save()

    messages.add_message(request, messages.INFO, "Done")


class SchoolFieldInline(admin.TabularInline):
    model = SchoolField

class SchoolFileAdmin(admin.ModelAdmin):
    inlines = [SchoolFieldInline]
    actions = [import_or_update_school_information]
admin.site.register(SchoolFile, SchoolFileAdmin)

class IndicatorFieldInline(admin.TabularInline):
    model = IndicatorField

class IndicatorFileAdmin(admin.ModelAdmin):
    inlines = [IndicatorFieldInline]
    actions = [import_indicator]
admin.site.register(IndicatorFile, IndicatorFileAdmin)

admin.site.register(DimensionName)
admin.site.register(DimensionFor)