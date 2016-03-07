from django.test import TestCase, Client
from django.core.urlresolvers import reverse
#from django.utils import timezone
from models import Dictionary, Category

# Create your tests here.
class DictionaryTermTest(TestCase):
    def test_create_dictionary_term(self):
        #Create new dictionary term
        term = Dictionary()
        cat = Category()
        
        #Add Dictionary term attributes
        cat.category = "Student Achievement"
        cat.save()
        
         #Test Category model
        all_cat = Category.objects.all()
        self.assertEqual(len(all_cat),1)
        
        only_cat = all_cat[0]
        self.assertEqual(only_cat, cat)
        
        #term.category = cat
        #term.term = "Accountability"
        #term.content = "Rhode Island's School Accountability System"
      
        #term.save()
        
        #term.category = cat
        #term.term = "PARCC"
        #term.content = "The PARCC Assessments are administered to children in Rhode Island schools"
        #term.save()
        
        term1 = Dictionary.objects.create(category=cat,term="Accountability",content="Rhode Island's School Accountability System")
        term2 = Dictionary.objects.create(category=cat,term="PARCC",content="The PARCC Assessments are administered to children in Rhode Island schools")
        
        #Test Dictionary model
        all_terms = Dictionary.objects.all()
        self.assertEqual(len(all_terms), 2)
        
        only_term = all_terms.filter(term="Accountability")[0]
        self.assertEqual(only_term, term1)
        
        self.assertEqual(only_term.category.category, "Student Achievement")
        self.assertEqual(only_term.term, "Accountability")
        self.assertEqual(only_term.content, "Rhode Island's School Accountability System")
       
        #term.category = cat
        #term.term = "PARCC"
        #term.content = "The PARCC Assessments are administered to children in Rhode Island schools"
        #term.save()
        
        #alls = Dictionary.objects.all()
        #self.assertEqual(len(alls), 2)
        
class DictionaryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        #Create new dictionary term
        term = Dictionary()
        cat = Category()
        #Add Dictionary term attributes
        cat.category = "Student Achievement"
        cat.save()
        
        term.category = cat
        term.term = "Accountability"
        term.content = "Rhode Island's School Accountability System"
        
        #Save it
        term.save()
        
        # Fetch index
        #esponse = self.client.get('/understanding-data/dictionary')
        response = self.client.get(reverse('dictionary'))
        self.assertEquals(response.status_code, 200)
        
         # Check the dictionary terms data is in the response
        #print response.content
        self.assertTrue(term.category.category in response.content)
        self.assertTrue(term.term in response.content)
        self.assertTrue(term.content in term.content)
        
    #    self.assertTrue(str(story.pub_date.year) in response.content)
    #    self.assertTrue(story.pub_date.strftime('%b') in response.content)
    #    self.assertTrue(str(story.pub_date.day) in response.content)