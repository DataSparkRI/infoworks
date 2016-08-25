from data.models import SchoolYear

from data.models import StateIndicator
from data.models import StateIndicatorData
from data.models import StateIndicatorDataSet

from data.models import DistrictIndicator
from data.models import DistrictIndicatorData
from data.models import DistrictIndicatorDataSet

from data.models import SchoolIndicator
from data.models import SchoolIndicatorData
from data.models import SchoolIndicatorDataSet

school_year_dic = {
'2009-10':'2009-2010',
'2010-11':'2010-2011',
'2011-12':'2011-2012',
'2012-13':'2012-2013',
'2013-14':'2013-2014',
'2014-15':'2014-2015'}

def fix_school():
    def copy(bad_year, school_year, indicator):
        school_year = SchoolYear.objects.get(school_year=school_year)
        good_year, created = SchoolIndicatorDataSet.objects.get_or_create(school_indicator=indicator,school_year=school_year)
        for each_year in bad_year:
            for each_data in each_year.data:
                indicator_data, created = SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=good_year, dimension_x=each_data.dimension_x, dimension_y=each_data.dimension_y)
                indicator_data.key_value = each_data.key_value
                indicator_data.data_type = each_data.data_type
                indicator_data.import_job = each_data.import_job
                indicator_data.save()
    def delete(bad_year):
        bad_year.delete()
    for indicator in SchoolIndicator.objects.all():
            #indicator = SchoolIndicator.objects.get(id=10)
        for key, value in school_year_dic.iteritems():
            bad_year = indicator.dataset.filter(school_year__school_year=key)
            if bad_year.count() > 0:
               print "School: Find bad year %s"%key
               copy(bad_year,value, indicator)
               delete(bad_year)

def fix_district():
    def copy(bad_year, school_year, indicator):
        school_year = SchoolYear.objects.get(school_year=school_year)
        good_year, created = DistrictIndicatorDataSet.objects.get_or_create(district_indicator=indicator,school_year=school_year)
        for each_year in bad_year:
            for each_data in each_year.data:
                indicator_data, created = DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=good_year, dimension_x=each_data.dimension_x, dimension_y=each_data.dimension_y)
                indicator_data.key_value = each_data.key_value
                indicator_data.data_type = each_data.data_type
                indicator_data.import_job = each_data.import_job
                indicator_data.save()
    def delete(bad_year):
        bad_year.delete()
    for indicator in DistrictIndicator.objects.all():
            #indicator = DistrictIndicator.objects.get(id=10)
        for key, value in school_year_dic.iteritems():
            bad_year = indicator.dataset.filter(school_year__school_year=key)
            if bad_year.count() > 0:
               print "District: Find bad year %s"%key
               copy(bad_year,value, indicator)
               delete(bad_year)

def fix_state():
    def copy(bad_year, school_year, indicator):
        school_year = SchoolYear.objects.get(school_year=school_year)
        good_year, created = StateIndicatorDataSet.objects.get_or_create(state_indicator=indicator,school_year=school_year)
        for each_year in bad_year:
            for each_data in each_year.data:
                indicator_data, created = StateIndicatorData.objects.get_or_create(state_indicator_dataset=good_year, dimension_x=each_data.dimension_x, dimension_y=each_data.dimension_y)
                indicator_data.key_value = each_data.key_value
                indicator_data.data_type = each_data.data_type
                indicator_data.import_job = each_data.import_job
                indicator_data.save()
    def delete(bad_year):
        bad_year.delete()
    for indicator in StateIndicator.objects.all():
            #indicator = StateIndicator.objects.get(id=10)
        for key, value in school_year_dic.iteritems():
            bad_year = indicator.dataset.filter(school_year__school_year=key)
            if bad_year.count() > 0:
               print "State: Find bad year %s"%key
               copy(bad_year,value, indicator)
               delete(bad_year)

fix_school()
fix_district()
fix_state()
for key, value in school_year_dic.iteritems():
    SchoolYear.objects.filter(school_year=key).delete()

