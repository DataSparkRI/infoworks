from data.models import IndicatorTitle
from data.models import StateIndicator
from data.models import StateIndicatorDataSet
from data.models import StateIndicatorData
from data.models import DistrictIndicator
from data.models import DistrictIndicatorDataSet
from data.models import DistrictIndicatorData
from data.models import SchoolIndicator
from data.models import SchoolIndicatorDataSet
from data.models import SchoolIndicatorData

indicator_title = 'Qualifications and Teacher-Student Ratio'
cp_indicator_title = 'Student-Teacher Ratio'
indicator_order = 2 # copyed indicator order

def copy_state_indicator(cp_title, cp_to_title, order):
   title = IndicatorTitle.objects.get(title=cp_title)
   copy_title, created = IndicatorTitle.objects.get_or_create(title=cp_to_title)
   indicators = StateIndicator.objects.filter(title = title)
   for indicator in indicators:
      cp_indicator, created = StateIndicator.objects.get_or_create(
                     state_indicator_set = indicator.state_indicator_set,
                     title = copy_title,
                     order = order,
                     short_title= indicator.short_title,
                     description = indicator.description,
                     data_indicator= indicator.data_indicator,
                     switch_highchart_xy = indicator.switch_highchart_xy,
                     over_time = indicator.over_time,
                     highchart = indicator.highchart
                     )
      for dataset in indicator.dataset:
          cp_dataset, created = StateIndicatorDataSet.objects.get_or_create(
             state_indicator=cp_indicator,
             school_year=dataset.school_year,
             description=dataset.description,
             csv_file=dataset.csv_file,
             data_type=dataset.data_type,
             import_file=dataset.import_file
          )
          for data in dataset.data:
             cp_data, created = StateIndicatorData.objects.get_or_create(
                state_indicator_dataset = cp_dataset,
                dimension_x = data.dimension_x,
                dimension_y = data.dimension_y,
                key_value = data.key_value,
                data_type = data.data_type,
                import_job = data.import_job)

def copy_district_indicator(cp_title, cp_to_title, order):
   title = IndicatorTitle.objects.get(title=cp_title)
   copy_title, created = IndicatorTitle.objects.get_or_create(title=cp_to_title)
   indicators = DistrictIndicator.objects.filter(title = title)
   for indicator in indicators:
      cp_indicator, created = DistrictIndicator.objects.get_or_create(
                     district_indicator_set = indicator.district_indicator_set,
                     title = copy_title,
                     order = order,
                     short_title= indicator.short_title,
                     description = indicator.description,
                     data_indicator= indicator.data_indicator,
                     switch_highchart_xy = indicator.switch_highchart_xy,
                     over_time = indicator.over_time,
                     highchart = indicator.highchart
                     )
      for dataset in indicator.dataset:
          cp_dataset, created = DistrictIndicatorDataSet.objects.get_or_create(
             district_indicator=cp_indicator,
             school_year=dataset.school_year,
             description=dataset.description,
             csv_file=dataset.csv_file,
             data_type=dataset.data_type,
             import_file=dataset.import_file
          )
          for data in dataset.data:
             cp_data, created = DistrictIndicatorData.objects.get_or_create(
                district_indicator_dataset = cp_dataset,
                dimension_x = data.dimension_x,
                dimension_y = data.dimension_y,
                key_value = data.key_value,
                data_type = data.data_type,
                import_job = data.import_job)

def copy_school_indicator(cp_title, cp_to_title, order):
   title = IndicatorTitle.objects.get(title=cp_title)
   copy_title, created = IndicatorTitle.objects.get_or_create(title=cp_to_title)
   indicators = SchoolIndicator.objects.filter(title = title)
   for indicator in indicators:
      cp_indicator, created = SchoolIndicator.objects.get_or_create(
                     school_indicator_set = indicator.school_indicator_set,
                     title = copy_title,
                     order = order,
                     short_title= indicator.short_title,
                     description = indicator.description,
                     data_indicator= indicator.data_indicator,
                     switch_highchart_xy = indicator.switch_highchart_xy,
                     over_time = indicator.over_time,
                     highchart = indicator.highchart
                     )
      for dataset in indicator.dataset:
          cp_dataset, created = SchoolIndicatorDataSet.objects.get_or_create(
             school_indicator=cp_indicator,
             school_year=dataset.school_year,
             description=dataset.description,
             csv_file=dataset.csv_file,
             data_type=dataset.data_type,
             import_file=dataset.import_file
          )
          for data in dataset.data:
             cp_data, created = SchoolIndicatorData.objects.get_or_create(
                school_indicator_dataset = cp_dataset,
                dimension_x = data.dimension_x,
                dimension_y = data.dimension_y,
                key_value = data.key_value,
                data_type = data.data_type,
                import_job = data.import_job)

copy_state_indicator(indicator_title, cp_indicator_title, indicator_order)
copy_district_indicator(indicator_title, cp_indicator_title,indicator_order)
copy_school_indicator(indicator_title, cp_indicator_title,indicator_order)
