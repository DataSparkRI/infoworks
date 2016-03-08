from django.test import TestCase
from django.core.files import File as Django_File
from django.test.client import RequestFactory
from django.contrib import admin
from data.models import SchoolYear
from dataimport.models import StateFile, StateField
from data.models import State, StateIndicatorSet
# Create your tests here.
#class Test404PageTestCase(TestCase):
#    def test_404(self):
#        response = self.client.get('/state')
#        self.assertTemplateUsed(response, '404.html')


class ImportStateFileTestCase(TestCase):
    def setUp(self):
        file = open('dataimport/test_files/test_statefile.csv')
        school_year, created = SchoolYear.objects.get_or_create(school_year="2014-2015")
        django_file = Django_File(file)
        state_file = StateFile.objects.create(school_year=school_year, file=django_file)
        self.state_file = state_file

        self.assertEqual(StateFile.objects.all().count(), 1)
        
        state_file = StateFile.objects.all()[0]
        
        state_code = StateField.objects.get(name="state_code", state_file=state_file)
        self.assertEqual(state_code.match_option, None)
        state_code.match_option = "STATE_CODE"
        state_code.save()
        
        state_name = StateField.objects.get(name="state_name", state_file=state_file)
        self.assertEqual(state_name.match_option, None)
        state_name.match_option = "STATE_NAME"
        state_name.save()
        
        address = StateField.objects.get(name="address1", state_file=state_file)
        self.assertEqual(address.match_option, None)
        address.match_option = "ADDRESS"
        address.save()
        
        city = StateField.objects.get(name="city", state_file=state_file)
        self.assertEqual(city.match_option, None)
        city.match_option = "CITY"
        city.save()
        
        state = StateField.objects.get(name="state", state_file=state_file)
        self.assertEqual(state.match_option, None)
        state.match_option = "STATE"
        state.save()
        
        zipcode = StateField.objects.get(name="zipcode", state_file=state_file)
        self.assertEqual(zipcode.match_option, None)
        zipcode.match_option = "ZIP"
        zipcode.save()
        
        lea_phone = StateField.objects.get(name="lea_phone", state_file=state_file)
        self.assertEqual(lea_phone.match_option, None)
        lea_phone.match_option = "PHONE"
        lea_phone.save()
        
        lea_web_site = StateField.objects.get(name="lea_web_site", state_file=state_file)
        self.assertEqual(lea_web_site.match_option, None)
        lea_web_site.match_option = "WEB_SITE"
        lea_web_site.save()
        
        superintendent = StateField.objects.get(name="Superintendent", state_file=state_file)
        self.assertEqual(superintendent.match_option, None)
        superintendent.match_option = "COMMISSIONER"
        superintendent.save()
        
        notes = StateField.objects.get(name="Notes", state_file=state_file)
        self.assertEqual(notes.match_option, None)
        notes.match_option = "DESCRIPTION"
        notes.save()
        
        number_of_student = StateField.objects.get(name="number_of_student", state_file=state_file)
        self.assertEqual(number_of_student.match_option, None)
        number_of_student.match_option = "NUMBER_STUDENT"
        number_of_student.save()
        
        number_of_teacher = StateField.objects.get(name="number_of_teacher", state_file=state_file)
        self.assertEqual(number_of_teacher.match_option, None)
        number_of_teacher.match_option = "NUMBER_TEACHER"
        number_of_teacher.save()
        
        number_of_school = StateField.objects.get(name="number_of_school", state_file=state_file)
        self.assertEqual(number_of_school.match_option, None)
        number_of_school.match_option = "NUMBER_SCHOOL"
        number_of_school.save()        
        
        from dataimport.admin import import_or_update_state_information
        
        queryset = StateFile.objects.all()
        rf = RequestFactory()
        request = rf.post(
        '/admin/app/model',   # url of the admin change list
        {
            '_selected_action': [],
            'action': 'import_or_update_state_information',
            'post': 'post', 
        }
        )
        
        import_or_update_state_information(admin.ModelAdmin, request, queryset)
        
        from data.admin import write_default_state_indicator_set
        
        queryset = State.objects.filter(state_code = "1")
        rf = RequestFactory()
        request = rf.post(
        '/admin/app/model',   # url of the admin change list
        {
            '_selected_action': [],
            'action': 'write_default_state_indicator_set',
            'post': 'post', 
        }
        )
        
        write_default_state_indicator_set(admin.ModelAdmin, request, queryset)
        
        
    def tearDown(self):
        import os
        os.remove(self.state_file.file.file.name)

    def test_create_state(self):

        state = State.objects.get(state_code=1)
        self.assertEqual(State.objects.all().count(), 2)
        
        self.assertEqual(state.state_name, "Rhode Island Public Schools")
        self.assertEqual(state.activate, True)
        self.assertEqual(state.number_of_student, 4432)
        self.assertEqual(state.number_of_teacher, 543)
        self.assertEqual(state.number_of_school, 123)
        self.assertEqual(state.website, "http://www.google.org")
        self.assertEqual(state.slug, "rhode-island-public-schools")
        self.assertEqual(state.commissioner, "Mdfa F. Dba")
        self.assertEqual(state.street, "111 abc Road")
        self.assertEqual(state.city, "Barrington")
        self.assertEqual(state.state, "RI")
        self.assertEqual(state.zip, "2806")
        self.assertEqual(state.phone, "8645234178")
        
        
        state = State.objects.get(state_code=1)
        
        indicator_set = StateIndicatorSet.objects.filter(state = state)
        
        self.assertEqual(indicator_set.count(), 6)
        self.assertEqual(indicator_set.get(title="Student Achievement").order, 1)
        self.assertEqual(indicator_set.get(title="Teaching").order, 2)
        self.assertEqual(indicator_set.get(title="Families and Communities").order, 3)
        self.assertEqual(indicator_set.get(title="Safe and Supportive Schools").order, 4)
        self.assertEqual(indicator_set.get(title="Funding and Resources").order, 5)
        self.assertEqual(indicator_set.get(title="Other").order, 6)
        
    def test_state_font_page(self):
        
        state = State.objects.get(state_code=1)
        self.assertEqual(state.default_state, False)
        state.default_state = True
        state.save()
        
        response = self.client.get('/state')
        self.assertTemplateUsed(response, 'front_page/state_report.html')
        self.assertContains(response, 'Rhode Island Public Schools')
        self.assertContains(response, 'Commissioner Mdfa F. Dba')
        self.assertContains(response, '111 abc Road Barrington RI 2806')
        self.assertContains(response, '8645234178')
        self.assertContains(response, '4432 Students')
        self.assertContains(response, '543 Teachers')
        self.assertContains(response, '123 Schools')
        
        self.assertContains(response, 'Student Achievement')
        self.assertContains(response, 'Teaching')
        self.assertContains(response, 'Families and Communities')
        self.assertContains(response, 'Safe and Supportive Schools')
        self.assertContains(response, 'Funding and Resources')
        self.assertContains(response, 'Other')
        
        response = self.client.get('/state/rhode-island-public-schools')
        self.assertTemplateUsed(response, 'front_page/state_report.html')
        self.assertContains(response, 'Rhode Island Public Schools')
        self.assertContains(response, 'Commissioner Mdfa F. Dba')
        self.assertContains(response, '111 abc Road Barrington RI 2806')
        self.assertContains(response, '8645234178')
        self.assertContains(response, '4432 Students')
        self.assertContains(response, '543 Teachers')
        self.assertContains(response, '123 Schools')
        
        self.assertContains(response, 'Student Achievement')
        self.assertContains(response, 'Teaching')
        self.assertContains(response, 'Families and Communities')
        self.assertContains(response, 'Safe and Supportive Schools')
        self.assertContains(response, 'Funding and Resources')
        self.assertContains(response, 'Other')
        
        response = self.client.get('/state/other-public-schools')
        self.assertTemplateUsed(response, 'front_page/state_report.html')
        
        