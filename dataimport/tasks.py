from celery import shared_task

@shared_task
def ImportIndicatorFile(queryset):
    from dataimport.actions.ImportIndicator import import_indicator
    import_indicator(queryset)
    return "SUCCESS"
