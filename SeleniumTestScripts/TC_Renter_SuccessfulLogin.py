import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TC_Renter_SuccessfulLogin(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):
        user = "testrenter_1"
        pwd = "user@123"

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
            logout_link = driver.find_element_by_xpath("/html/body/section/div[1]/div[1]/div/div[2]/div/ul/li/div/a[2]").text
            if "Logout" in logout_link:
                print("TC_Renter_SuccessfulLogin - User Successfully logged in")
                assert True
            else:
                assert False

        except NoSuchElementException:
            self.fail("TC_Renter_SuccessfulLogin - Login Failed - user may not exist")
            assert False

        try:
            # attempt to find the 'username' - when user logs in
            greetings = driver.find_element_by_xpath(
                "/html/body/section/div[1]/div[1]/div/div[2]/div/ul/li/div/a[1]").text
            if "Hello "+ user in greetings:
                print("TC_Renter_SuccessfulLogin - User Name is displayed correctly")
                assert True
            else:
                print("TC_Renter_SuccessfulLogin - User Name is not displayed correctly")
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
