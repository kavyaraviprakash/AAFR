import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date

class TC_Renter_Navbar_links_validation(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_aafr(self):
        user = "testrenter_1"
        pwd = "user@123"
        # Login Page
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
        # Navigation to Find a Park page
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div/nav/div[2]/ul/li[2]/a")
        elem.click()
        time.sleep(3)
        try:
            # attempt to find the ParkList Title
            FindParkPage = driver.current_url
            if "https://dry-reef-78127.herokuapp.com/view/" in FindParkPage:
                print("TC_Renter_Navbar_links_validation - User is navigated to Find a Park Page")
                assert True
            else:
                assert False

        except NoSuchElementException:
            self.fail("TC_Renter_Navbar_links_validation - User is not navigated to Find a Park Page")
            assert False
        # Navigation to Events Calendar Page
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div/nav/div[2]/ul/li[3]/a")
        elem.click()
        time.sleep(3)
        try:
            # attempt to find the ParkList Title
            today = date.today()
            currentMonth = today.strftime("%B")
            currentYear = str(today.year)
            Expected_MonthYear = currentMonth +" "+ currentYear
            Month = driver.find_element_by_xpath("/html/body/section/div[2]/center/table/tbody/tr[1]/th").text
            if Expected_MonthYear in Month:
                print("TC_Renter_Navbar_links_validation - User is navigated to Events Calendar Page and calendar is displayed for:"+Expected_MonthYear)
                assert True
            else:
                assert False

        except NoSuchElementException:
            self.fail("TC_Renter_Navbar_links_validation - Either User is not navigated to Events Calendar Page or calendar is not current month and year, displayed calendar month and year is:"+Expected_MonthYear)
            assert False
        # Navigation to Contact Us Page
        elem = driver.find_element_by_xpath("/html/body/section/div[1]/div[2]/div/div/div/div/div/nav/div[2]/ul/li[4]/a")
        elem.click()
        time.sleep(3)
        try:
            # attempt to find the ParkList Title
            ContactPage = driver.current_url
            if "https://dry-reef-78127.herokuapp.com/contact_page/" in ContactPage:
                print("TC_Renter_Navbar_links_validation - User is navigated to Contact Page")
                assert True
            else:
                assert False

        except NoSuchElementException:
            self.fail("TC_Renter_Navbar_links_validation - User is not navigated to Contact Page")
            assert False
        elem = driver.find_element_by_xpath(
            "/html/body/section/div[1]/div[2]/div/div/div/div/div/nav/div[2]/ul/li[1]/a")
        elem.click()
        time.sleep(3)
        try:
            # attempt to find the ParkList Title
            HomePage = driver.current_url
            if "https://dry-reef-78127.herokuapp.com/renters_homepage/" in HomePage:
                print("TC_Renter_Navbar_links_validation - User is navigated to Home Page")
                assert True
            else:
                assert False

        except NoSuchElementException:
            self.fail("TC_Renter_Navbar_links_validation - User is not navigated to Home Page")
            assert False

    @classmethod
    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
