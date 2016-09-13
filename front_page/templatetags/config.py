from django import template
from front_page.models import Config
from data.models import SchoolIndicatorDataSet, StateIndicatorDataSet, DistrictIndicatorDataSet, DistrictIndicator, StateIndicator
from data.models import SchoolYear

register = template.Library()

@register.simple_tag
def get_history_info_year(dimension_x, count):
    return dimension_x[count-1]

@register.simple_tag
def get_history_info(type, get):
    from data.models import State, District, School
    state = None
    district = None
    school = None
    dimension_y = [school.school_year for school in SchoolYear.objects.all().order_by("school_year")]

    table = {"dimension_x": ["Topic","Category"] + dimension_y, "data":[]}
    
    def getData(obj):
        result = []
        for indicator_set in obj.indicatorset:
            data = []
            for indicator in indicator_set.indicators:
                data = [indicator_set.title]
                data.append(indicator.title.title)
                for school_year in dimension_y:
                    try:
                        indicator.dataset.get(school_year__school_year=school_year)
                        data.append(True)
                    except:
                        data.append(None)
                result.append(data)
        return result
    
    def returnDefaultState():
        state = State.objects.get(default_state=True)
        table["name"] = state.state_name
        table["description"] = state.description
        return getData(state)
    

    if type == "state":
            try:
                state = State.objects.get(slug=get)
                table["name"] = state.state_name
                table["description"] = state.description
                table["data"] = getData(state)
            except:
                table["data"] = returnDefaultState()
    elif type == "district":
            try:
                district = District.objects.get(slug=get)
                table["name"] = district.district_name
                table["description"] = district.description
                table["data"] = getData(district)
            except:
                table["data"] = returnDefaultState()
    elif type == "school":
            try:
                school = School.objects.get(slug=get)
                table["name"] = school.school_name
                table["description"] = school.description
                table["data"] = getData(school)
            except:
                table["data"] = returnDefaultState()
    else:
            table["data"] = returnDefaultState()
    return table



@register.filter(name='get_config')
def get_config(config_name):
    try:
        return Config.objects.get(name=config_name).value
    except:
        return None

@register.simple_tag
def get_data_type(value, data_type):
    
    if value == '-1':
        return "too few data"
    elif value == '' or value == ' ':
        return 'no data'

    if data_type == 'NUMERIC':
        return value
    elif data_type == 'NUMERIC_COMMA':
        try:
            return format(value, ',d')
        except:
            return value
    elif data_type == 'PERCENT':
        return str(value)+'%'
    elif data_type == 'RATIO':
        return '1:'+str(value)
    elif data_type == 'DOLLARS':
        return '$'+str(value)
    elif data_type == 'DOLLARS_COMMA':
        try:
            return '$' + '{0:,.2f}'.format(float(value))
        except:
            return value
    else:
        return str(value)   


@register.simple_tag
def get_display(data):
    
    try:
        indicator = data.school_indicator_dataset.school_indicator
    except:
        try:
            indicator = data.district_indicator_dataset.district_indicator
        except:
            try:
                indicator = data.state_indicator_dataset.state_indicator
            except:
                return "no data"
    
    if indicator.title.custom_value.count() == 0 and (indicator.title.data_type == None or indicator.title.data_type == '') and indicator.title.rounding_decimal_place == 0:
        if data.key_value == '-1':
            return "too few data"
        elif data.key_value == '' or data.key_value == ' ':
            return 'no data'
        elif data.data_type == 'NUMERIC':
            split = data.key_value.split('.')
            if len(split) == 1:
                return '{0:,.0f}'.format(float(data.key_value))
            else:
                type = '{0:,.'+str(len(split[1]))+'f}'
                return type.format(float(data.key_value))
        elif data.data_type == 'STRING':
            return data.key_value
        elif data.data_type == 'PERCENT':
            return data.key_value+'%'
        elif data.data_type == 'RATIO':
            return '1:'+data.key_value
        else:
            return data.key_value
            
    rounding_decimal_place = indicator.title.rounding_decimal_place
    #if rounding_decimal_place == None:
    #    rounding_decimal_place = 0
    value = data.key_value
    if data.data_type == 'STRING':
        value = data.key_value
        for custom in indicator.title.custom_value:
            if custom.operator == '=':
                if value == float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
                else:
                    return value
            elif custom.operator == '!=':
                if value != float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
                else:
                    return value
        
    else:
        if rounding_decimal_place > 0:
            try:
               value = round(float(value),rounding_decimal_place)
            except:
                value = data.key_value
        elif rounding_decimal_place <= 0:
            try:
               value = int(round(float(value),rounding_decimal_place))
            except:
                value = data.key_value
        else:
            value = data.key_value
        for custom in indicator.title.custom_value:
            if custom.operator == '>':
                if float(value) > float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value

            elif custom.operator == '>=':
                if float(value) >= float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
               
            elif custom.operator == '<':

                if float(value) < float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value

            elif custom.operator == '<=':
                if float(value) <= float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
          
            elif custom.operator == '=':
                if float(value) == float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
              
            elif custom.operator == '!=':
                if float(value) != float(custom.value) and (custom.display_value != None or custom.display_value != ''):
                    return custom.display_value
             
            else:
                pass

        if indicator.title.data_type != None or indicator.title.data_type != '':
            return get_data_type(value, indicator.title.data_type)
    return get_data_type(value, data.data_type)

@register.simple_tag
def get_school_indicator_value(school, indicator, school_year, dimension_y):
    try:
        school_indicator_dataset = SchoolIndicatorDataSet.objects.get(school_indicator__school_indicator_set__school=school, school_indicator__title=indicator.title, school_year__school_year=school_year)
        return school_indicator_dataset.get_objects('This School', dimension_y)
    except:
        return None

@register.simple_tag
def get_school_history_value(school_indicator, dimension_y, dimension_x='This School'):
    try:
        for school_year in SchoolYear.objects.all().order_by('-school_year'):
            try:
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
def get_district_indicator_value(district, indicator, school_year, dimension_y):
    try:
        district_indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator__district_indicator_set__district=district, district_indicator__title=indicator.title, school_year__school_year=school_year)
        return district_indicator_dataset.get_objects('This District', dimension_y)
    except:
        return None

@register.simple_tag
def get_district_history_value(district_indicator, dimension_y, dimension_x='This District'):
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
def get_state_indicator_value(state, indicator, school_year, dimension_y):
    try:
        state_indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator__state_indicator_set__state=state, state_indicator__title=indicator.title, school_year__school_year=school_year)
        return state_indicator_dataset.get_objects('Statewide', dimension_y)
    except:
        return None
    
@register.simple_tag
def get_state_history_value(state_indicator, dimension_y, dimension_x="Statewide"):
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
