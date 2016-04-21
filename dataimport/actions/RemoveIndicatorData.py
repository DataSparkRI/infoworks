from data.models import StateIndicatorData, DistrictIndicatorData, SchoolIndicatorData

def all_data(q):
    if q.state_indicator:
        data = StateIndicatorData.objects.filter(import_job=q)
    if q.district_indicator:
        data = DistrictIndicatorData.objects.filter(import_job=q)
    if q.school_indicator:
        data = SchoolIndicatorData.objects.filter(import_job=q)
    return data

def remove_indicator(queryset):
    for q in queryset:
        data = all_data(q)
        data.delete()
        