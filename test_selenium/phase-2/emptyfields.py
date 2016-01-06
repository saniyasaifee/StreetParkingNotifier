from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Emptyfields(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_emptyfields(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Street Parking Notfier").click()
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_id("logout").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("hjshajdkhaskjdhaskjd")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("nmma,nsdkasdlkasjdlkas")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath("//div[3]/a/span").click()
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_link_text("Sign Up").click()
        driver.find_element_by_link_text("Sign in").click()
        driver.find_element_by_css_selector("a > span").click()
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