from django import template
from front_page.models import Config
from data.models import SchoolIndicatorDataSet, StateIndicatorDataSet, DistrictIndicatorDataSet

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
def get_district_indicator_value(district, school_year, dimension_y):
    try:
        district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator__district_indicator_set__district=district, school_year__school_year=school_year)
        return district_indicator_dataset.get_objects('This District', dimension_y)
    except:
        return None

@register.simple_tag
def get_state_indicator_value(state, school_year, dimension_y):
    try:
        state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator__state_indicator_set__state=state, school_year__school_year=school_year)
        return state_indicator_dataset.get_objects('Statewide', dimension_y)
    except:
        return None