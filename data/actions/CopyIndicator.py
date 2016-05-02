from data.models import DistrictIndicator, DistrictDisplayData, DistrictDisplayDataY, \
StateIndicator, StateDisplayData, StateDisplayDataY, \
SchoolIndicator, SchoolDisplayData, SchoolDisplayDataY

def copy_district_indicator(queryset):
    
    def copy_district_display_data(q, district_indicator):
        display_data = DistrictDisplayData.objects.filter(district_indicator = q)
        DistrictDisplayData.objects.filter(district_indicator = district_indicator).delete()
        for data in display_data:
            DistrictDisplayData.objects.get_or_create(district_indicator = district_indicator,
                                                      display = data.display,
                                                      display_name=data.display_name,
                                                      order = data.order)
        
    def copy_display_data_y(q, district_indicator):
        display_data_y = DistrictDisplayDataY.objects.filter(district_indicator = q)
        DistrictDisplayDataY.objects.filter(district_indicator = district_indicator).delete()
        for data in display_data_y:
            DistrictDisplayDataY.objects.get_or_create(district_indicator = district_indicator,
                                                       display = data.display,
                                                       display_name = data.display_name,
                                                       order=data.order,
                                                       detail=data.detail)
    
    count = queryset.count()
    if count == 1:
        for q in queryset:
            title = q.title
            district_indicators = DistrictIndicator.objects.filter(title=title).exclude(id=q.id)
            for district_indicator in district_indicators:
                district_indicator.over_time = q.over_time
                district_indicator.save()
                copy_district_display_data(q, district_indicator)
                copy_display_data_y(q, district_indicator)
        return "SUCCESS"
    else:
        return "ERROR Please select only one"
    
def copy_state_indicator(queryset):
    
    def copy_state_display_data(q, state_indicator):
        display_data = StateDisplayData.objects.filter(state_indicator = q)
        StateDisplayData.objects.filter(state_indicator = state_indicator).delete()
        for data in display_data:
            StateDisplayData.objects.get_or_create(state_indicator = state_indicator,
                                                      display = data.display,
                                                      display_name=data.display_name,
                                                      order = data.order)
        
    def copy_display_data_y(q, state_indicator):
        display_data_y = StateDisplayDataY.objects.filter(state_indicator = q)
        StateDisplayDataY.objects.filter(state_indicator = state_indicator).delete()
        for data in display_data_y:
            StateDisplayDataY.objects.get_or_create(state_indicator = state_indicator,
                                                       display = data.display,
                                                       display_name = data.display_name,
                                                       order=data.order,
                                                       detail=data.detail)
    
    count = queryset.count()
    if count == 1:
        for q in queryset:
            title = q.title
            state_indicators = StateIndicator.objects.filter(title=title).exclude(id=q.id)
            for state_indicator in state_indicators:
                state_indicator.over_time = q.over_time
                state_indicator.save()
                copy_state_display_data(q, state_indicator)
                copy_display_data_y(q, state_indicator)
        return "SUCCESS"
    else:
        return "ERROR Please select only one"
    
def copy_school_indicator(queryset):
    
    def copy_school_display_data(q, school_indicator):
        display_data = SchoolDisplayData.objects.filter(school_indicator = q)
        SchoolDisplayData.objects.filter(school_indicator = school_indicator).delete()
        for data in display_data:
            SchoolDisplayData.objects.get_or_create(school_indicator = school_indicator,
                                                      display = data.display,
                                                      display_name=data.display_name,
                                                      order = data.order)
        
    def copy_display_data_y(q, school_indicator):
        display_data_y = SchoolDisplayDataY.objects.filter(school_indicator = q)
        SchoolDisplayDataY.objects.filter(school_indicator = school_indicator).delete()
        for data in display_data_y:
            SchoolDisplayDataY.objects.get_or_create(school_indicator = school_indicator,
                                                       display = data.display,
                                                       display_name = data.display_name,
                                                       order=data.order,
                                                       detail=data.detail)
    
    count = queryset.count()
    if count == 1:
        for q in queryset:
            title = q.title
            school_indicators = SchoolIndicator.objects.filter(title=title).exclude(id=q.id)
            for school_indicator in school_indicators:
                school_indicator.over_time = q.over_time
                school_indicator.save()
                copy_school_display_data(q, school_indicator)
                copy_display_data_y(q, school_indicator)
        return "SUCCESS"
    else:
        return "ERROR Please select only one"