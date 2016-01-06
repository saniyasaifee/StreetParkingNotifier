from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class ShareInFacebook(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://parkingonstreet.herokuapp.com/contactus/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_share_in_facebook(self):
        driver = self.driver
        driver.get(self.base_url + "/contactus/")
        driver.find_element_by_id("logout").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=_e_0Fxy | ]]
        driver.find_element_by_id("u_0_1").click()
        driver.find_element_by_name("share").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=fdc58970e44a02 | ]]
        # ERROR: Caught exception [ERROR: Unsupported command [waitForPopUp | _blank | 30000]]
        # ERROR: Caught exception [ERROR: Unsupported command [waitForPopUp | _blank | 30000]]
    
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
