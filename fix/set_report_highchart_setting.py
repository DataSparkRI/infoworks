from data.models import IndicatorTitle
from data.models import DistrictIndicator
from data.models import DistrictDisplayDataYDetail
from data.models import SchoolIndicator
from data.models import SchoolDisplayDataYDetail

indicator_title = "Race/Ethnicity"
district_highchart_slug = 'students-from-various-racialethnic-backgrounds'
school_highchart_slug = 'students-from-various-racialethnic-backgrounds'

title = IndicatorTitle.objects.get(title=indicator_title)

highchart = DistrictDisplayDataYDetail.objects.get(slug=district_highchart_slug)
for indicator in DistrictIndicator.objects.filter(title=title):
   indicator.highchart = highchart
   indicator.save()

highchart = SchoolDisplayDataYDetail.objects.get(slug=school_highchart_slug)
for indicator in SchoolIndicator.objects.filter(title=title):
   indicator.highchart = highchart
   indicator.save()

