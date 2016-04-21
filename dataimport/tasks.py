from celery import shared_task

@shared_task
def ImportIndicatorFileData(queryset):
    from dataimport.actions.ImportIndicator import import_indicator
    import_indicator(queryset)
    return "SUCCESS"

@shared_task
def RemoveIndicatorFileData(queryset):
    from dataimport.actions.RemoveIndicatorData import remove_indicator
    remove_indicator(queryset)
    return "SUCCESS"

