from data.models import IndicatorTitle
from data.models import DistrictIndicator
from data.models import DistrictOverTime
from data.models import SchoolIndicator
from data.models import SchoolOverTime

#indicator_title = "Student Services"
#district_over_time_name = "Student-Characteristics-district-overtime"
#school_over_time_name = "Student-Characteristics-school-overtime"

indicator_title = "Race/Ethnicity"
district_over_time_name = "Race/Ethnicity overtime"
school_over_time_name = "Race/Ethnicity overtime"

title = IndicatorTitle.objects.get(title=indicator_title)

district_over_time = DistrictOverTime.objects.get(name=district_over_time_name)
for indicator in DistrictIndicator.objects.filter(title=title):
   indicator.over_time = district_over_time
   indicator.save()

school_over_time = SchoolOverTime.objects.get(name=school_over_time_name)
for indicator in SchoolIndicator.objects.filter(title=title):
   indicator.over_time = school_over_time
   indicator.save()

