from selenium import webdriver
import unittest
from django.test import TestCase
from locations.models import Locatiom
import locations.views 

# Create your tests here.
#class LocationTestCase(unittest.TestCase):
class LoginTestCase(TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
    
  def tearDown(self):
    self.browser.quit()
      
  def test_can_start_lgin(self):
    self.browser.get('http://127.0.0.1:8000')
  
    self.assertIn('Log in', self.browser.title)
    self.fail('Finish the test!')
  
if __name__ == '__main__':
  unittest.main(warnings='ignore')


