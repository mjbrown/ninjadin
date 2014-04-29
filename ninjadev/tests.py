from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from ninjadev.models import Character

# Create your tests here.
class CharacterTests(TestCase):
    
    def test_str(self):
        user = Character(name="Gazongas")
        self.assertEquals(str(user), "Gazongas")
        
        
class CharacterListIntegrationTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(CharacterListIntegrationTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CharacterListIntegrationTests, cls).tearDownClass()
        
    def test_character_listed(self):
        
        # Create a test character
        Character.objects.create(name="Gazongas", gender="Male")
        
        # Make sure it is listed
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.character')[0].text,
            'Gazongas' )
        