import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class TC_Renter_RentPark(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):

        pwd = "user@123"
        user = "testrenter_1"
        bbcourturl = "https://dry-reef-78127.herokuapp.com/1/basketball-court"

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
        elem = driver.find_element_by_xpath("/html/body/section/div[2]/div/div/div[1]/div/div[2]/a")
        elem.click()
        time.sleep(3)
        parkNames = driver.find_elements_by_xpath("//table/tbody/tr/td/a")
        links = list(parkNames)
        links[0].click()
        time.sleep(3)
        jcp = list(driver.find_elements_by_xpath("//div/center/a"))
        jcp[1].click()
        time.sleep(3)
        elem = (driver.find_element_by_xpath("//select/option[text()='5pm-7pm']")).click()
        elem = driver.find_element_by_name("Event_Date")
        tomorrow = date.today() + timedelta(1)
        elem.send_keys(tomorrow.strftime('%m/%d/%Y'))
        elem = driver.find_element_by_name("Team_Size")
        elem.send_keys("15")
        elem = driver.find_element_by_xpath("//form/input[@value='Rent']")
        elem.click()
        time.sleep(3)
        elem = driver.find_element_by_name("buy_now_btn")
        elem.click()
        time.sleep(3)
        elem = driver.find_element_by_id("buy_now_btn")
        elem.click()
        time.sleep(5)
        #elem.click()
        elem = driver.find_element_by_id("email")
        elem.send_keys("kavyaravi39@gmail.com")
        elem = driver.find_element_by_id("cardNumber")
        elem.send_keys("4242424242424242")
        elem = driver.find_element_by_id("cardExpiry")
        elem.send_keys("0924")
        elem = driver.find_element_by_id("cardCvc")
        elem.send_keys("123")
        elem = driver.find_element_by_id("billingName")
        elem.send_keys("kavyaravi39")
        elem = driver.find_element_by_id("billingPostalCode")
        elem.send_keys("68125")
        elem = driver.find_element_by_id("//form/div/div/button[@type='submit']")
        elem.click()
        try:
            elem = driver.find_element_by_xpath("//div/h1").text
            if (elem == "Payment Sucessful !!!"):
                print("TC_Renter_RentPark - Albuquerque Athletic Field Reservation Successful")
                assert True

            else:
                print("TC_Renter_RentPark - Albuquerque Athletic Field Reservation Unsuccessful")
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
