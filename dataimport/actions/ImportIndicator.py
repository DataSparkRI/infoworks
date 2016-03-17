
import csv
from django.contrib import messages
from dataimport.models import IndicatorFile, IndicatorField, DimensionName
from data.models import SchoolIndicator, SchoolIndicatorDataSet, SchoolIndicatorData, \
DistrictIndicator, DistrictIndicatorDataSet, DistrictIndicatorData, \
StateIndicator, StateIndicatorDataSet, StateIndicatorData, SchoolYear

def get_or_none(objects, match_option):
    try:
        objs = objects.filter(match_option=match_option)
        if objs.count() == 0:
            return None
        else:
            return objs
    except:
        return None

def get_index_or_none(headers, option):
    try:
        return headers.index(option)
    except:
        return None

def all_indicator(q):
    if q.state_indicator:
        indicators = StateIndicator.objects.filter(title=q.indicator)
    if q.district_indicator:
        indicators = DistrictIndicator.objects.filter(title=q.indicator)
    if q.school_indicator:
        indicators = SchoolIndicator.objects.filter(title=q.indicator)
    return indicators

def get_index(headers, dimension):
    index = {}
    
    for x in dimension:
        index.update({get_index_or_none(headers, x.name):
                        {'name':x.match_option, 'data_type':x.data_type, 'dimension_name':x.dimension_name}})
    return index
    
def get_lookup_table(fields, header, file_code):
    field = fields.get(name=header)

    if field.lookup_table != None:
        return field.lookup_table
    else:
        return None
    

def build_y_dimension_title(fields, headers, row, add_on_01,add_on_02,add_on_03,add_on_04,add_on_05,add_on_06,add_on_07,add_on_08,add_on_09,add_on_10):
    result = ""
    if add_on_01 != None:
        index = get_index_or_none(headers, add_on_01[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + table.get_code(row[index]) + " "
        else:
            result = result + row[index] + " "
    if add_on_02 != None:
        index = get_index_or_none(headers, add_on_02[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + headers[index] + " " + table.get_code(row[index]) + " "
        else:
            result = result + headers[index] + " " + row[index] + " "
    if add_on_03 != None:
        index = get_index_or_none(headers, add_on_03[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + table.get_code(row[index]) + " "
        else:
            result = result + row[index] + " "
    if add_on_04 != None:
        index = get_index_or_none(headers, add_on_04[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + headers[index] + " " + table.get_code(row[index]) + " "
        else:
            result = result + headers[index] + " " + row[index] + " "
    if add_on_05 != None:
        index = get_index_or_none(headers, add_on_05[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + table.get_code(row[index]) + " "
        else:
            result = result + row[index] + " "
    if add_on_06 != None:
        index = get_index_or_none(headers, add_on_06[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + headers[index] + " " + table.get_code(row[index]) + " "
        else:
            result = result + headers[index] + " " + row[index] + " "
    if add_on_07 != None:
        index = get_index_or_none(headers, add_on_07[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + table.get_code(row[index]) + " "
        else:
            result = result + row[index] + " "
    if add_on_08 != None:
        index = get_index_or_none(headers, add_on_08[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + headers[index] + " " + table.get_code(row[index]) + " "
        else:
            result = result + headers[index] + " " + row[index] + " "
    if add_on_09 != None:
        index = get_index_or_none(headers, add_on_09[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + table.get_code(row[index]) + " "
        else:
            result = result + row[index] + " "
    if add_on_10 != None:
        index = get_index_or_none(headers, add_on_10[0].name)
        table = get_lookup_table(fields, headers[index], row[index])
        if table != None:
            result = result + headers[index] + " " + table.get_code(row[index]) + " "
        else:
            result = result + headers[index] + " " + row[index] + " "
    return result

def import_indicator(modeladmin, request, queryset):
    for q in queryset:
        path = q.file.path
        fields = IndicatorField.objects.filter(indicator_file=q)
        
        state_codes = get_or_none(fields, "STATE_CODE")
        district_codes = get_or_none(fields, "DISTRICT_CODE") #queryset
        school_codes = get_or_none(fields,"SCHOOL_CODE") #queryset
        dimension = get_or_none(fields,"DIMENSION") #queryset
        school_year = get_or_none(fields, "SCHOOL_YEAR") #queryset
        add_on_01 = get_or_none(fields, "01_ADD_ON") #queryset
        add_on_02 = get_or_none(fields, "02_ADD_ON_WITH_HEADER") #queryset
        add_on_03 = get_or_none(fields, "03_ADD_ON") #queryset
        add_on_04 = get_or_none(fields, "04_ADD_ON_WITH_HEADER") #queryset
        add_on_05 = get_or_none(fields, "05_ADD_ON") #queryset
        add_on_06 = get_or_none(fields, "06_ADD_ON_WITH_HEADER") #queryset
        add_on_07 = get_or_none(fields, "07_ADD_ON") #queryset
        add_on_08 = get_or_none(fields, "08_ADD_ON_WITH_HEADER") #queryset
        add_on_09 = get_or_none(fields, "09_ADD_ON") #queryset
        add_on_10 = get_or_none(fields, "10_ADD_ON_WITH_HEADER") #queryset


        if q.indicator != None:
            indicators = all_indicator(q) #indicators queryset
        
        if q.state_indicator:
            with open(path) as f:
                reader = csv.reader(f)
                headers = reader.next()
                state_code_index = get_index_or_none(headers, state_codes[0].name)
                
                
                index = get_index(headers, dimension)
                if school_year != None:
                    school_year_index = get_index_or_none(headers, school_year[0].name)
                else:
                    school_year_index = None
                
                for row in reader:
                    try:
                        state_code = row[state_code_index]
                        if state_code == '' or state_code == ' ':
                            continue
                    except:
                        break
                    try:
                        indicator = indicators.get(state_indicator_set__state__state_code=state_code)
                    except:
                        try:
                            indicator = indicators.filter(state_indicator_set__state__default_state = True)[0]
                        except:
                            indicator = None
                    if indicator != None: # if do have indicator
                        if q.school_year != None:
                            state_indicator_dataset, created = StateIndicatorDataSet.objects.get_or_create(state_indicator=indicator, school_year=q.school_year)
                        else:
                            school_year_obj, created = SchoolYear.objects.get_or_create(school_year = row[school_year_index])
                            state_indicator_dataset, created = StateIndicatorDataSet.objects.get_or_create(state_indicator=indicator, school_year=school_year_obj)

                        dimension_y_add_on = build_y_dimension_title(fields, headers,row,add_on_01,add_on_02,add_on_03,add_on_04,add_on_05,add_on_06,add_on_07,add_on_08,add_on_09,add_on_10)


                        for key, value in index.iteritems():
                            
                            dimension_y_name = "%s%s"%(dimension_y_add_on, value["dimension_name"].name)
                            DimensionName.objects.get_or_create(name=dimension_y_name)
                            StateIndicatorData.objects.get_or_create(state_indicator_dataset=state_indicator_dataset,
                                                            dimension_x = q.indicator_for,
                                                            dimension_y = dimension_y_name,
                                                            key_value = row[key],
                                                            data_type = value["data_type"],
                                                            import_job = q
                            )
        
        if q.district_indicator:
            with open(path) as f:
                reader = csv.reader(f)
                headers = reader.next()
                district_code_index = get_index_or_none(headers, district_codes[0].name)
                
                
                index = get_index(headers, dimension)
                if school_year != None:
                    school_year_index = get_index_or_none(headers, school_year[0].name)
                else:
                    school_year_index = None
                
                for row in reader:
                    try:
                        district_code = row[district_code_index]
                        if district_code == '' or district_code == ' ':
                            continue
                    except:
                        break
                    try:
                        indicator = indicators.get(district_indicator_set__district__district_code=district_code)
                    except:
                        indicator = None
                    if indicator != None: # if do have indicator
                        if q.school_year != None:
                            district_indicator_dataset, created = DistrictIndicatorDataSet.objects.get_or_create(district_indicator=indicator, school_year=q.school_year)
                        else:
                            school_year_obj, created = SchoolYear.objects.get_or_create(school_year = row[school_year_index])
                            district_indicator_dataset, created = DistrictIndicatorDataSet.objects.get_or_create(district_indicator=indicator, school_year=school_year_obj)

                        dimension_y_add_on = build_y_dimension_title(fields, headers,row,add_on_01,add_on_02,add_on_03,add_on_04,add_on_05,add_on_06,add_on_07,add_on_08,add_on_09,add_on_10)


                        for key, value in index.iteritems():
                            
                            dimension_y_name = "%s%s"%(dimension_y_add_on, value["dimension_name"].name)
                            DimensionName.objects.get_or_create(name=dimension_y_name)
                            DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=district_indicator_dataset,
                                                            dimension_x = q.indicator_for,
                                                            dimension_y = dimension_y_name,
                                                            key_value = row[key],
                                                            data_type = value["data_type"],
                                                            import_job = q
                            )
                            #if created:
                            #    DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=district_indicator_dataset,
                            #                                dimension_x = "School Year",
                            #                                dimension_y = value["dimension_name"].name,
                            #                                key_value = q.school_year.school_year,
                            #                                data_type = "STRING",
                            #                                import_job = q
                            #    )

        if q.school_indicator:
            with open(path) as f:
                reader = csv.reader(f)
                headers = reader.next()
                school_code_index = get_index_or_none(headers, school_codes[0].name)
                
                
                index = get_index(headers, dimension)
                if school_year != None:
                    school_year_index = get_index_or_none(headers, school_year[0].name)
                else:
                    school_year_index = None
                
                for row in reader:
                    try:
                        school_code = row[school_code_index]
                        if school_code == '' or school_code == ' ':
                            continue
                    except:
                        break
                    try:
                        indicator = indicators.get(school_indicator_set__school__school_code=school_code)
                    except:
                        indicator = None
                    if indicator != None: # if do have indicator
                        if q.school_year != None:
                            school_indicator_dataset, created = SchoolIndicatorDataSet.objects.get_or_create(school_indicator=indicator, school_year=q.school_year)
                        else:
                            school_year_obj, created = SchoolYear.objects.get_or_create(school_year = row[school_year_index])
                            school_indicator_dataset, created = SchoolIndicatorDataSet.objects.get_or_create(school_indicator=indicator, school_year=school_year_obj)

                        dimension_y_add_on = build_y_dimension_title(fields, headers,row,add_on_01,add_on_02,add_on_03,add_on_04,add_on_05,add_on_06,add_on_07,add_on_08,add_on_09,add_on_10)


                        for key, value in index.iteritems():
                            
                            dimension_y_name = "%s%s"%(dimension_y_add_on, value["dimension_name"].name)
                            DimensionName.objects.get_or_create(name=dimension_y_name)
                            SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=school_indicator_dataset,
                                                            dimension_x = q.indicator_for,
                                                            dimension_y = dimension_y_name,
                                                            key_value = row[key],
                                                            data_type = value["data_type"],
                                                            import_job = q
                            )
            
        
            
