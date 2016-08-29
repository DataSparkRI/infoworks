from data.models import IndicatorTitle
from data.models import StateIndicator
from data.models import StateIndicatorDataSet
from data.models import DistrictIndicator
from data.models import DistrictIndicatorDataSet
from data.models import SchoolIndicator
from data.models import SchoolIndicatorDataSet

four_year_lookup = {
'2008-2009':'Students Entering Grade 9 in 2005-06',
'2009-2010':'Students Entering Grade 9 in 2006-07',
'2010-2011':'Students Entering Grade 9 in 2007-08',
'2011-2012':'Students Entering Grade 9 in 2008-09',
'2012-2013':'Students Entering Grade 9 in 2009-10',
'2013-2014':'Students Entering Grade 9 in 2010-11',
'2014-2015':'Students Entering Grade 9 in 2011-12'
}

five_year_lookup = {
'2008-2009':'Students Entering Grade 9 in 2004-05',
'2009-2010':'Students Entering Grade 9 in 2005-06',
'2010-2011':'Students Entering Grade 9 in 2006-07',
'2011-2012':'Students Entering Grade 9 in 2007-08',
'2012-2013':'Students Entering Grade 9 in 2008-09',
'2013-2014':'Students Entering Grade 9 in 2009-10',
'2014-2015':'Students Entering Grade 9 in 2010-11'
}

four_year = IndicatorTitle.objects.get(title='Four Year Graduation Rate')
five_year = IndicatorTitle.objects.get(title='Five Year Graduation Rate')

def save_dataset(dataset, lookup):
      try:
         description = lookup[dataset.school_year.school_year]
         dataset.description = description
         dataset.save()
      except:
         pass

def fix_state_district_school(title, lookup):
   for indicators in StateIndicator.objects.filter(title=title):
      for datasets in StateIndicatorDataSet.objects.filter(state_indicator=indicators):
         save_dataset(datasets, lookup)
   
   for indicators in DistrictIndicator.objects.filter(title=title):
      for datasets in DistrictIndicatorDataSet.objects.filter(district_indicator=indicators):
         save_dataset(datasets,lookup)
   
   for indicators in SchoolIndicator.objects.filter(title=title):
      for datasets in SchoolIndicatorDataSet.objects.filter(school_indicator=indicators):
         save_dataset(datasets,lookup)

fix_state_district_school(four_year, four_year_lookup)
fix_state_district_school(five_year, five_year_lookup)
