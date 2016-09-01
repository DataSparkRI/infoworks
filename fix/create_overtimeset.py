from data.models import StateOverTimeSet
from data.models import DistrictOverTimeSet
from data.models import SchoolOverTimeSet
from data.models import IndicatorTitle

for title in IndicatorTitle.objects.all():
   name = title.title
   StateOverTimeSet.objects.get_or_create(name=name)
   DistrictOverTimeSet.objects.get_or_create(name=name)
   SchoolOverTimeSet.objects.get_or_create(name=name)

from data.models import StateIndicator
from data.models import DistrictIndicator
from data.models import SchoolIndicator

for indicator in StateIndicator.objects.all():
   indicator.over_time = StateOverTimeSet.objects.get(name=indicator.title.title)
   indicator.save()
   print "State: Save %s"%indicator.title.title

for indicator in DistrictIndicator.objects.all():
   indicator.over_time = DistrictOverTimeSet.objects.get(name=indicator.title.title)
   indicator.save()
   print "District: Save %s"%indicator.title.title

for indicator in SchoolIndicator.objects.all():
   indicator.over_time = SchoolOverTimeSet.objects.get(name=indicator.title.title)
   indicator.save()
   print "School: Save %s"%indicator.title.title

print "Done"
