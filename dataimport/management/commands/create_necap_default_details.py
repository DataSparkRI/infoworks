from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys

class Command(BaseCommand):

    help = ''

    def handle(self, *args, **options):
        import os
        from data.models import SchoolDisplayDataYDetail
        def create_detail_set(detail):
            from data.models import SchoolDisplayDataYDetailSet
            SchoolDisplayDataYDetailSet.objects.get_or_create(detail=detail, name="School vs Statewide", title="School vs Statewide", order=1)
            SchoolDisplayDataYDetailSet.objects.get_or_create(detail=detail, name="Ethnicity and Migrant Status", title="Ethnicity and Migrant Status", order=2)
            SchoolDisplayDataYDetailSet.objects.get_or_create(detail=detail, name="Poverty and Gender", title="Poverty and Gender", order=3)
            SchoolDisplayDataYDetailSet.objects.get_or_create(detail=detail, name="Disabilities and ELL", title="Disabilities and ELL", order=4)
        
        def create_school():
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 1st Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 2nd Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 3th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 4th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 5th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 6th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 7th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 8th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 9th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 10th Grade Math")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 11th Grade Math")
            create_detail_set(detail)
            
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 1st Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 2nd Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 3th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 4th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 5th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 6th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 7th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 8th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 9th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 10th Grade Reading")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 11th Grade Reading")
            create_detail_set(detail)
            
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 1st Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 2nd Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 3th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 4th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 5th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 6th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 7th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 8th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 9th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 10th Grade Writing")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 11th Grade Writing")
            create_detail_set(detail)
            
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 1st Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 2nd Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 3th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 4th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 5th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 6th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 7th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 8th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 9th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 10th Grade Science")
            create_detail_set(detail)
            detail, created = SchoolDisplayDataYDetail.objects.get_or_create(name="School NECAP 11th Grade Science")
            create_detail_set(detail)
        
        from data.models import DistrictDisplayDataY, DistrictDisplayData, DistrictIndicator, IndicatorTitle
        from dataimport.models import DimensionFor, DimensionName
        title = IndicatorTitle.objects.get(title='NECAP Assessments')
        district_indicators = DistrictIndicator.objects.filter(title=title)
        
        #clean
        for indicator in district_indicators:
            DistrictDisplayData.objects.filter(district_indicator = indicator).delete()
            DistrictDisplayDataY.objects.filter(district_indicator = indicator).delete()
        
        
        for indicator in district_indicators:
            
            display, created = DimensionFor.objects.get_or_create(name = "This District")
            DistrictDisplayData.objects.get_or_create(district_indicator = indicator, display = display, order=1)
            display, created = DimensionFor.objects.get_or_create(name = "Statewide")
            DistrictDisplayData.objects.get_or_create(district_indicator = indicator, display = display, order=2)
            
            display, created = DimensionName.objects.get_or_create(name="3rd Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display = display, order =1, display_name="3rd Grade Math")
            display, created = DimensionName.objects.get_or_create(name="3rd Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display = display, order =2, display_name="3rd Grade Reading")
      
            display, created = DimensionName.objects.get_or_create(name="4th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =3, display_name="4th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="4th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =4, display_name="4th Grade Reading")
            display, created = DimensionName.objects.get_or_create(name="4th Grade Science All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =5, display_name="4th Grade Science")
           
            display, created = DimensionName.objects.get_or_create(name="5th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =6, display_name="5th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="5th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =7, display_name="5th Grade Reading")
            display, created = DimensionName.objects.get_or_create(name="5th Grade Writing All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =8, display_name="5th Grade Writing")

            display, created = DimensionName.objects.get_or_create(name="6th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =9, display_name="6th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="6th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =10, display_name="6th Grade Reading")
            
            display, created = DimensionName.objects.get_or_create(name="7th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =11, display_name="7th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="7th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =12, display_name="7th Grade Reading")

            display, created = DimensionName.objects.get_or_create(name="8th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =13, display_name="8th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="8th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =14, display_name="8th Grade Reading")
            display, created = DimensionName.objects.get_or_create(name="8th Grade Writing All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =15, display_name="8th Grade Writing")
            display, created = DimensionName.objects.get_or_create(name="8th Grade Science All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =16, display_name="8th Grade Science")

            display, created = DimensionName.objects.get_or_create(name="11th Grade Math All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =17, display_name="11th Grade Math")
            display, created = DimensionName.objects.get_or_create(name="11th Grade Reading All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =18, display_name="11th Grade Reading")
            display, created = DimensionName.objects.get_or_create(name="11th Grade Writing All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =19, display_name="11th Grade Writing")
            display, created = DimensionName.objects.get_or_create(name="11th Grade Science All Students: All Students % Proficient")
            district, created = DistrictDisplayDataY.objects.get_or_create(district_indicator = indicator, display=display, order =20, display_name="11th Grade Science")
            
            