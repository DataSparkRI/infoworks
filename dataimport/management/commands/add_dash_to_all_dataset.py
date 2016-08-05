from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys
from data.models import DistrictIndicatorDataSet
from data.models import DistrictIndicatorData
from data.models import StateIndicatorDataSet
from data.models import StateIndicatorData
from data.models import SchoolIndicatorDataSet
from data.models import SchoolIndicatorData

class Command(BaseCommand):

    help = ''

    def handle(self, *args, **options):
        import os
        for dataset in StateIndicatorDataSet.objects.all():
            StateIndicatorData.objects.get_or_create(state_indicator_dataset=dataset,
               dimension_x = 'Statewide',
               dimension_y = 'Dash',
               key_value = '--',
               data_type = 'STRING')

        for dataset in DistrictIndicatorDataSet.objects.all():
            DistrictIndicatorData.objects.get_or_create(district_indicator_dataset=dataset,
               dimension_x = 'This District',
               dimension_y = 'Dash',
               key_value = '--',
               data_type = 'STRING')

        for dataset in SchoolIndicatorDataSet.objects.all():
            SchoolIndicatorData.objects.get_or_create(school_indicator_dataset=dataset,
               dimension_x = 'This School',
               dimension_y = 'Dash',
               key_value = '--',
               data_type = 'STRING')

