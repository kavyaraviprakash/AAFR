import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TC_Renter_UnsuccessfulLogin(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):
        user = "testrenter_1"
        pwd = "user@12345"
        expected_msg = "Username OR password is incorrect"
        driver = self.driver
        driver.maximize_window()
        driver.get("https://dry-reef-78127.herokuapp.com/loginuser/")
        elem = driver.find_element_by_name("username")
        elem.send_keys(user)
        elem = driver.find_element_by_name("password")
        elem.send_keys(pwd)
        time.sleep(5)
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/div/button")
        elem.click()
        time.sleep(3)
        try:
            # attempt to find the 'logout' - if found, logged in
            errormsg = driver.find_element_by_xpath("/html/body/section/div[2]/div/form").text
            if expected_msg in errormsg:
                print("TC_Renter_UnsuccessfulLogin - Invalid Username/Password Validation Successful")
                assert True
            else:
                print("TC_Renter_UnsuccessfulLogin - Invalid Username/Password Validation unsuccessful")
                assert False

        except NoSuchElementException:
            self.fail("NoSuchElementException")
            assert False


    @classmethod
    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
