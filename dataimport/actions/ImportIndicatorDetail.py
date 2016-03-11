
import csv
from django.contrib import messages
from dataimport.models import IndicatorFile, IndicatorField, IndicatorDetailFile, IndicatorDetailField
from data.models import SchoolIndicator, SchoolIndicatorDataSet, SchoolIndicatorData, \
DistrictIndicator, DistrictIndicatorDataSet, DistrictIndicatorData, \
StateIndicator, StateIndicatorDataSet, StateIndicatorData
from data.models import DistrictIndicatorDetailDataSet, DistrictIndicatorDetailData

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
    if q.district_indicator:
        indicators = DistrictIndicator.objects.filter(title=q.indicator)
    if q.school_indicator:
        indicators = SchoolIndicator.objects.filter(title=q.indicator)
    if q.state_indicator:
        indicators = StateIndicator.objects.filter(title=q.indicator)
    return indicators

def get_index(headers, dimension):
    index = {}
    
    for x in dimension:
        index.update({get_index_or_none(headers, x.name):
                        {'name':x.match_option, 'data_type':x.data_type, 'dimension_name':x.dimension_name}})
    return index




def import_indicator_detail(modeladmin, request, queryset):
    for q in queryset:
        path = q.file.path
        fields = IndicatorDetailField.objects.filter(indicator_detail_file=q)
        
        district_codes = get_or_none(fields, "DISTRICT_CODE") #queryset
        school_codes = get_or_none(fields,"SCHOOL_CODE") #queryset
        dimension = get_or_none(fields,"DIMENSION") #queryset
        
        if q.indicator != None:
            indicators = all_indicator(q) #indicators queryset
        
        if q.state_indicator:
            with open(path) as f:
                reader = csv.reader(f)
                headers = reader.next()
                state_code_index = get_index_or_none(headers, state_codes[0].name)
                index = get_index(headers, dimension)
                
                for row in reader:
                    try:
                        state_code = row[state_code_index]
                    except:
                        break
                    try:
                        indicator = indicators.get(state_indicator_set__state__state_code=state_code)
                    except:
                        indicator = None
                    if indicator != None: # if do have indicator
                        state_indicator_dataset, created = StateIndicatorDataSet.objects.get_or_create(state_indicator=indicator, school_year=q.school_year)
                        for key, value in index.iteritems():

                            StateIndicatorData.objects.get_or_create(state_indicator_dataset=state_indicator_dataset,
                                                            dimension_x = q.indicator_for,
                                                            dimension_y = value["dimension_name"].name,
                                                            key_value = row[key],
                                                            data_type = value["data_type"],
                                                            import_job = q
                            )
        
        if q.district_indicator:
            if q.indicator != None and q.school_year != None and q.dimension_name != None and q.category != None:
                with open(path) as f:
                    reader = csv.reader(f)
                    headers = reader.next()
                    district_code_index = get_index_or_none(headers, district_codes[0].name)
                    index = get_index(headers, dimension)
                    
                    

                    for row in reader:
                        try:
                            district_code = row[district_code_index]
                        except:
                            break
                        try:
                            indicator = indicators.get(district_indicator_set__district__district_code=district_code)
                        except:
                            indicator = None
                        if indicator != None: # if do have indicator
                            
                            #Get or Create indicator dataset
                            district_indicator_dataset, created = DistrictIndicatorDataSet.objects.get_or_create(district_indicator=indicator, school_year=q.school_year)
                            
                            #Get or Create indicator data with dimension_name as dimension_y, and Details as dimension_x
                            indicator_data, created = DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=district_indicator_dataset,
                                                                dimension_x = 'Details',
                                                                dimension_y = q.dimension_name.name,
                                                                key_value = 'NULL',
                                                                data_type = 'SUBDATASET',
                            )
                            
                            #Get or Greate District Indicator Detail DataSet
                            
                            district_indicator_detail_dataset, created = DistrictIndicatorDetailDataSet.objects.get_or_create(indicator_data=indicator_data, title = q.category, display_type="TABLE")
                            
                            print q.category
                            
                            for key, value in index.iteritems():

                                DistrictIndicatorDetailData.objects.get_or_create(district_indicator_detail_dataset=district_indicator_detail_dataset,
                                                                dimension_x = q.indicator_for,
                                                                dimension_y = value["dimension_name"].name,
                                                                key_value = row[key],
                                                                data_type = value["data_type"],
                                                                import_job = q
                                )
                                
                            
        if q.school_indicator:
            with open(path) as f:
                reader = csv.reader(f)
                headers = reader.next()
                school_code_index = get_index_or_none(headers, school_codes[0].name)
                index = get_index(headers, dimension)
                
                for row in reader:
                    try:
                        school_code = row[school_code_index]
                    except:
                        break
                    try:
                        indicator = indicators.get(school_indicator_set__school__school_code=school_code)
                    except:
                        indicator = None
                    if indicator != None: # if do have indicator
                        school_indicator_dataset, created = SchoolIndicatorDataSet.objects.get_or_create(school_indicator=indicator, school_year=q.school_year)
                        for key, value in index.iteritems():

                            SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=school_indicator_dataset,
                                                            dimension_x = q.indicator_for,
                                                            dimension_y = value["dimension_name"].name,
                                                            key_value = row[key],
                                                            data_type = value["data_type"],
                                                            import_job = q
                            )
                            #if created:
                            #    SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=school_indicator_dataset,
                            #                                dimension_x = "School Year",
                            #                                dimension_y = value["dimension_name"].name,
                            #                                key_value = q.school_year.school_year,
                            #                                data_type = "STRING",
                            #                                import_job = q
                            #    )


    messages.add_message(request, messages.INFO, "Done")
            
        
            
