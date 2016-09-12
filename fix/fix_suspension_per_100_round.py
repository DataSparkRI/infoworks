from data.models import StateIndicatorData
from data.models import DistrictIndicatorData
from data.models import SchoolIndicatorData

rounding_decimal_place = 1
list_dimension_y = ['Suspensions per 100 Students (Elementary School)', 'Suspensions per 100 Students (Middle School)', 'Suspensions per 100 Students (High School)', 'Suspensions per 100 Students (All Grades)']

for dimension_y in list_dimension_y:
   indicators = StateIndicatorData.objects.filter(dimension_y = dimension_y)
   for data in indicators:
      try:
         data.key_value = round(float(data.key_value),rounding_decimal_place)
         data.save()
      except:
         pass
   indicators = DistrictIndicatorData.objects.filter(dimension_y = dimension_y)
   for data in indicators:
      try:
         data.key_value = round(float(data.key_value),rounding_decimal_place)
         data.save()
      except:
         pass
   indicators = SchoolIndicatorData.objects.filter(dimension_y = dimension_y)
   for data in indicators:
      try:
         data.key_value = round(float(data.key_value),rounding_decimal_place)
         data.save()
      except:
         pass

