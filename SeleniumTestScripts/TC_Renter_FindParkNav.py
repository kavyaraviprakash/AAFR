import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TC_Renter_FindParkNav(unittest.TestCase):
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
        #park_list = driver.find_elements_by_xpath("//a[text() = 'Jerry Cline Park']")
        #links = list(park_list)
        #links [0].click()
        parkNames = driver.find_elements_by_xpath("//table/tbody/tr/td/a")
        links = list(parkNames)
        #locating park_list table.
        #mytable = driver.find_elements_by_xpath("/html/body/section/div[2]/div/div[2]/table/tbody")
        #locate rows of table
        rows = len(driver.find_elements_by_xpath("//table/tbody/tr"))
        cols = len(driver.find_elements_by_xpath("//table/tbody/tr[1]/td"))
        try:
            if "Jerry Cline Park" in links[0].text:
                print("Jerry Cline Park is listed in the table")
                links[0].click()
                time.sleep(3)
                jcp = list(driver.find_elements_by_xpath("//div/center/a"))
                if "1-Jerry Basketball court" in jcp[1].text:
                    print("TC_Renter_FindParkNav - 1-Jerry Basketball court link present")
                    jcp[1].click()
                    time.sleep(3)
                    elem = driver.current_url
                    if elem == bbcourturl:
                        print("TC_Renter_FindParkNav - User Successfully naviageted to Rent BBCourt page")
                        assert True
                    else:
                        print("TC_Renter_FindParkNav - User was not successfully naviageted to Rent BBCourt page")
                else:
                    print("TC_Renter_FindParkNav - 1-Jerry Basketball court link not present")
                    assert False

            else:
                print("TC_Renter_FindParkNav - Jerry Cline Park is not listed in the table")
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
