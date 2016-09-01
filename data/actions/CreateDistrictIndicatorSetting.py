from data.models import District, DistrictDisplayDataSetting, DistrictDisplayDataYSetting, \
DistrictIndicator, DistrictDisplayData, DistrictDisplayDataY

def copy_district_display_data_setting(q, district_indicator):
	settings = DistrictDisplayDataSetting.objects.filter(title = q).order_by('order')
	DistrictDisplayData.objects.filter(district_indicator = district_indicator).delete()
	for data in settings:
		DistrictDisplayData.objects.get_or_create(district_indicator = district_indicator,
												display = data.display,
												display_name=data.display_name,
												order = data.order)

def clean_district_display_data_y(q):
	for district_indicator in DistrictIndicator.objects.filter(title=q):
		DistrictDisplayDataY.objects.filter(district_indicator=district_indicator).delete()

def add_district_display_data_setting_y(data, district_indicator):
	DistrictDisplayDataY.objects.get_or_create(district_indicator = district_indicator,
											display = data.display,
											display_name = data.display_name,
											order=data.order,
											detail=data.detail,
											prefix=data.prefix,
											suffix=data.suffix)

def create_indicator(queryset):
	for q in queryset:
		for district_indicator in DistrictIndicator.objects.filter(title=q):
			copy_district_display_data_setting(q, district_indicator)
		
		clean_district_display_data_y(q)
		
		for setting in DistrictDisplayDataYSetting.objects.filter(title = q).order_by('order'):
			for district_indicator in DistrictIndicator.objects.filter(title=q):
				add_district_display_data_setting_y(setting, district_indicator)
	return "SUCCESS"