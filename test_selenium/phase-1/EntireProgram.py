from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Seleniumtest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://streetparking-notifier.herokuapp.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("mithila")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("mith")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("sign up").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("mithila")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mithilachwdhry@gmail.com")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("1234")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("1234")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("mithila")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("12345")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        Select(driver.find_element_by_id("id_boroughcode")).select_by_visible_text("Manhattan")
        driver.find_element_by_id("id_main_street").clear()
        driver.find_element_by_id("id_main_street").send_keys("washington ave")
        driver.find_element_by_id("id_from_street").clear()
        driver.find_element_by_id("id_from_street").send_keys("180 st")
        driver.find_element_by_id("id_to_street").clear()
        driver.find_element_by_id("id_to_street").send_keys("185st")
        Select(driver.find_element_by_id("id_direction")).select_by_visible_text("W")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_id("id_to_street").clear()
        driver.find_element_by_id("id_to_street").send_keys("190st")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
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
