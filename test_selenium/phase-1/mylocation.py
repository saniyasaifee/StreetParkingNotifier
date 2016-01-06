from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Mylocation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://streetparking-notifier.herokuapp.com/whereiam/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_mylocation(self):
        driver = self.driver
        driver.get(self.base_url + "/whereiam/")
        Select(driver.find_element_by_id("id_boroughcode")).select_by_visible_text("Manhattan")
        driver.find_element_by_id("id_main_street").clear()
        driver.find_element_by_id("id_main_street").send_keys("washington ave")
        driver.find_element_by_id("id_from_street").clear()
        driver.find_element_by_id("id_from_street").send_keys("180st")
        driver.find_element_by_id("id_to_street").clear()
        driver.find_element_by_id("id_to_street").send_keys("145st")
        Select(driver.find_element_by_id("id_direction")).select_by_visible_text("W")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
