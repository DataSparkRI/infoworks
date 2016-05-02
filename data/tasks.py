from celery import shared_task

@shared_task
def CopyDistrictIndicatorData(queryset):
    from data.actions.CopyIndicator import copy_district_indicator
    message = copy_district_indicator(queryset)
    return message

@shared_task
def CopyStateIndicatorData(queryset):
    from data.actions.CopyIndicator import copy_state_indicator
    message = copy_state_indicator(queryset)
    return message

@shared_task
def CopySchoolIndicatorData(queryset):
    from data.actions.CopyIndicator import copy_school_indicator
    message = copy_school_indicator(queryset)
    return message

@shared_task
def CreateSchoolIndicatorSetting(queryset):
    from data.actions.CreateSchoolIndicatorSetting import create_indicator
    message = create_indicator(queryset)
    return message
