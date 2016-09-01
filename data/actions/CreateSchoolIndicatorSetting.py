from data.models import School, SchoolDisplayDataSetting, SchoolDisplayDataYSetting, \
SchoolIndicator, SchoolDisplayData, SchoolDisplayDataY

def copy_school_display_data_setting(q, school_indicator):
	settings = SchoolDisplayDataSetting.objects.filter(title = q).order_by('order')
	SchoolDisplayData.objects.filter(school_indicator = school_indicator).delete()
	for data in settings:
		SchoolDisplayData.objects.get_or_create(school_indicator = school_indicator,
												display = data.display,
												display_name=data.display_name,
												order = data.order)

def clean_school_display_data_y(q):
	for school_indicator in SchoolIndicator.objects.filter(title=q):
		SchoolDisplayDataY.objects.filter(school_indicator=school_indicator).delete()

def add_school_display_data_setting_y(data, school_indicator):
	SchoolDisplayDataY.objects.get_or_create(school_indicator = school_indicator,
											display = data.display,
											display_name = data.display_name,
											order=data.order,
											detail=data.detail,
											prefix=data.prefix,
											suffix=data.suffix)

def create_indicator(queryset):
	for q in queryset:
		for school_indicator in SchoolIndicator.objects.filter(title=q):
			copy_school_display_data_setting(q, school_indicator)
		
		clean_school_display_data_y(q)
		
		for setting in SchoolDisplayDataYSetting.objects.filter(title = q).order_by('order'):
			if setting.grade_level == 'ALL':
				for school_indicator in SchoolIndicator.objects.filter(title=q):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='ELEMENTARY':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__elementary_school=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='MIDDLE':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__middle_school=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='HIGH':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__high_school=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_PK':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_pk=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_K':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_k=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_1':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_1=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_2':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_2=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_3':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_3=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_4':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_4=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_5':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_5=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_6':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_6=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_7':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_7=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_8':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_8=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_9':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_9=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_10':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_10=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_11':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_11=True):
					add_school_display_data_setting_y(setting, school_indicator)
			elif setting.grade_level =='GRADE_12':
				for school_indicator in SchoolIndicator.objects.filter(title=q, school_indicator_set__school__grade_12=True):
					add_school_display_data_setting_y(setting, school_indicator)
	return "SUCCESS"