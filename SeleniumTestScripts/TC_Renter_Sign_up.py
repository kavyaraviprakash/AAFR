import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TC_Renter_Sign_up(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):

        homepage = "https://dry-reef-78127.herokuapp.com/renters_homepage/"

        driver = self.driver
        driver.maximize_window()
        driver.get("https://dry-reef-78127.herokuapp.com/")
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[1]/div/div[2]/div/ul/li[2]/div/a")
        elem.click()
        time.sleep(5)
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[1]/td/input")
        elem.send_keys("testrenter_3")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[2]/td/input")
        elem.send_keys("kavyaravi39@gmail.com")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[3]/td/input")
        elem.send_keys("Abcde@123")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[4]/td/input")
        elem.send_keys("Abcde@123")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[5]/td/input")
        elem.send_keys("Nebraska")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[6]/td/input")
        elem.send_keys("68116")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[7]/td/input")
        elem.send_keys("1234567890")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[8]/td/input")
        elem.send_keys("user@123")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/table/tbody/tr[9]/td/input")
        elem.send_keys("user@123")
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/form/button")
        elem.click()
        time.sleep(5)

        elem = driver.current_url
        if elem == homepage:
            print("TC_Renter_Sign_up - Submit button on SignUp page Navigated user to Home Page Verified")
            assert True
        else:
            print("TC_Renter_Sign_up - User is not navigated to HomePage as expected.Instead navigated to" + elem)
            assert False

    @classmethod
    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
