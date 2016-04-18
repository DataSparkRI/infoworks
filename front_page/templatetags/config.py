from django import template
from front_page.models import Config
from data.models import SchoolIndicatorDataSet, StateIndicatorDataSet, DistrictIndicatorDataSet, DistrictIndicator, StateIndicator
from data.models import SchoolYear

register = template.Library()

@register.filter(name='get_config')
def get_config(config_name):
    try:
        return Config.objects.get(name=config_name).value
    except:
        return None

@register.simple_tag
def get_school_indicator_value(school, school_year, dimension_y):
    try:
        school_indicator_dataset = SchoolIndicatorDataSet.objects.get(school_indicator__school_indicator_set__school=school, school_year__school_year=school_year)
        return school_indicator_dataset.get_objects('This School', dimension_y)
    except:
        return None

@register.simple_tag
def get_school_history_value(school_indicator, dimension_y, dimension_x):
    print school_indicator, dimension_y, dimension_x
    try:
        for school_year in SchoolYear.objects.all().order_by('-school_year'):
            try:
                print school_indicator, school_year
                print SchoolIndicatorDataSet.objects.filter(school_indicator=school_indicator, school_year__school_year=school_year)
                school_indicator_dataset = SchoolIndicatorDataSet.objects.get(school_indicator=school_indicator, school_year__school_year=school_year)
                data = school_indicator_dataset.get_objects(dimension_x, dimension_y)
            except:
                data = None
            if data != None:
                return data
        return None
    except:
        return None
    
@register.simple_tag
def get_school_value(school_indicator, str_school_year, dimension_y, dimension_x):
    if dimension_x == '' or dimension_x == None or str_school_year == None or str_school_year =='':
        return None
    
    school_year = SchoolYear.objects.get(school_year=str_school_year)
    school_indicator_dataset = SchoolIndicatorDataSet.objects.get(school_indicator = school_indicator, school_year__school_year=school_year)
    data = school_indicator_dataset.get_objects(dimension_x, dimension_y)
    if data == None:
        district = school_indicator.school_indicator_set.school.district
        district_indicator = DistrictIndicator.objects.get(district_indicator_set__district=district, title=school_indicator.title)
        school_year = SchoolYear.objects.get(school_year=str_school_year)
        district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator = district_indicator, school_year__school_year=school_year)
        data = district_indicator_dataset.get_objects(dimension_x, dimension_y)
        if data == None:
            state = district.us_state
            state_indicator = StateIndicator.objects.get(state_indicator_set__state=state, title=school_indicator.title)
            school_year = SchoolYear.objects.get(school_year=str_school_year)
            state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator=state_indicator, school_year__school_year=school_year)
            data = state_indicator_dataset.get_objects(dimension_x, dimension_y)
            return data
        else:
            return data
    else:
        return data

@register.simple_tag
def get_district_indicator_value(district, school_year, dimension_y):
    try:
        district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator__district_indicator_set__district=district, school_year__school_year=school_year)
        return district_indicator_dataset.get_objects('This District', dimension_y)
    except:
        return None

@register.simple_tag
def get_district_history_value(district_indicator, dimension_y, dimension_x):
    try:
        for school_year in SchoolYear.objects.all().order_by('-school_year'):
            try:
                district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator=district_indicator, school_year__school_year=school_year)
                data = district_indicator_dataset.get_objects(dimension_x, dimension_y)
            except:
                data = None
            if data != None:
                return data
        return None
    except:
        return None
    
@register.simple_tag
def get_district_value(district_indicator, str_school_year, dimension_y, dimension_x):
    if dimension_x == '' or dimension_x == None or str_school_year == None or str_school_year =='':
        return None
    
    school_year = SchoolYear.objects.get(school_year=str_school_year)
    district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator=district_indicator, school_year__school_year=school_year)
    data = district_indicator_dataset.get_objects(dimension_x, dimension_y)
    if data == None:
        state = district_indicator.district_indicator_set.district.us_state
        state_indicator = StateIndicator.objects.get(state_indicator_set__state=state, title=district_indicator.title)
        school_year = SchoolYear.objects.get(school_year=str_school_year)
        state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator=state_indicator, school_year__school_year=school_year)
        data = state_indicator_dataset.get_objects(dimension_x, dimension_y)
        return data
    else:
        return data

@register.simple_tag
def get_state_indicator_value(state, school_year, dimension_y):
    try:
        state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator__state_indicator_set__state=state, school_year__school_year=school_year)
        return state_indicator_dataset.get_objects('Statewide', dimension_y)
    except:
        return None
    
@register.simple_tag
def get_state_history_value(state_indicator, dimension_y, dimension_x):
    try:
        for school_year in SchoolYear.objects.all().order_by('-school_year'):
            try:
                state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator=state_indicator, school_year__school_year=school_year)
                data = state_indicator_dataset.get_objects(dimension_x, dimension_y)
            except:
                data = None
            if data != None:
                return data
        return None
    except:
        return None
    
@register.simple_tag
def get_state_value(state_indicator, school_year, dimension_y, dimension_x):
    if dimension_x == '' or dimension_x == None or school_year == None or school_year =='':
        return None
    try:
        school_year = SchoolYear.objects.get(school_year=school_year)
        state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator=state_indicator, school_year__school_year=school_year)
        data = state_indicator_dataset.get_objects(dimension_x, dimension_y)
        return data
    except:
        return None