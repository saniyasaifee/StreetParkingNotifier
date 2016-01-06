from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class EditProfileInfo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://parkingonstreet.herokuapp.com/whereiam/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_edit_profile_info(self):
        driver = self.driver
        driver.get(self.base_url + "/whereiam/")
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_link_text("edit profile").click()
        driver.find_element_by_id("id_form-0-username").clear()
        driver.find_element_by_id("id_form-0-username").send_keys("mithila")
        driver.find_element_by_id("id_form-0-first_name").clear()
        driver.find_element_by_id("id_form-0-first_name").send_keys("mithila")
        driver.find_element_by_id("id_form-0-last_name").clear()
        driver.find_element_by_id("id_form-0-last_name").send_keys("chowdhury")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_link_text("edit profile").click()
        driver.find_element_by_id("id_form-0-first_name").clear()
        driver.find_element_by_id("id_form-0-first_name").send_keys("mithila")
        driver.find_element_by_id("id_form-0-last_name").clear()
        driver.find_element_by_id("id_form-0-last_name").send_keys("chowdhury")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_link_text("edit profile").click()
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
