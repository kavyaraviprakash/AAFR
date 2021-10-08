import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TC_Renter_Edit_Profile(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):
        user = "autorenter_01"
        pwd = "user@123"

        driver = self.driver
        driver.maximize_window()
        driver.get("https://dry-reef-78127.herokuapp.com/loginuser/")
        elem = driver.find_element_by_name("username")
        elem.send_keys(user)
        elem = driver.find_element_by_name("password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/div/button")
        elem.click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[1]/div/div[2]/div/ul/li/a")
        elem.click()
        time.sleep(3)
        value = driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]/input[@type='email']")
        value = value.get_attribute('value')
        x = value.split("@")
        y = x[0].split('_')
        y[1] = int(y[1]) + 1
        updatedemail = y[0] + "_" + str(y[1]) + "@gmail.com"
        elem = driver.find_element_by_xpath("//table/tbody/tr/td/input[@name='email']")
        elem.clear()
        elem.send_keys(updatedemail)
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/div/button")
        elem.click()
        time.sleep(3)
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[1]/div/div[2]/div/ul/li/a")
        elem.click()
        time.sleep(3)
        actualupdatedemail = driver.find_element_by_name("email").get_attribute('value')
        try:
            # attempt to find the 'username' - when user logs in
            if updatedemail == actualupdatedemail:
                print("TC_Renter_Edit_Profile - User Profile Successfully Updated and Validated")
                assert True
            else:
                print("TC_Renter_Edit_Profile - User Profile is not Updated as expected")
                assert False

        except NoSuchElementException:
            self.fail(NoSuchElementException)
            assert False


    @classmethod
    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
