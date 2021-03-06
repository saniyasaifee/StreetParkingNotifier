from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class SettingsToLogout(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_settings_to_logout(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("mithila")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Settings").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_css_selector("span.arrow.next").click()
        driver.find_element_by_xpath("(//input[@value='remember-me'])[2]").click()
        driver.find_element_by_xpath("(//input[@value='remember-me'])[3]").click()
        driver.find_element_by_xpath("(//input[@value='remember-me'])[3]").click()
        driver.find_element_by_xpath("(//input[@value='remember-me'])[2]").click()
        Select(driver.find_element_by_id("hour")).select_by_visible_text("1 hour")
        driver.find_element_by_name("emailaddress").clear()
        driver.find_element_by_name("emailaddress").send_keys("myemail@gmail.com")
        driver.find_element_by_name("phonenumber").clear()
        driver.find_element_by_name("phonenumber").send_keys("212-314-1122")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("logout").click()
    
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
