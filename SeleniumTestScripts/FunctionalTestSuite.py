import unittest
from SeleniumTestScripts.TC_Renter_FindParkNav import TC_Renter_FindParkNav
from SeleniumTestScripts.TC_Renter_RentPark import TC_Renter_RentPark
from SeleniumTestScripts.TC_Renter_Edit_Profile import TC_Renter_Edit_Profile


TC_Renter_FindParkNav = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_FindParkNav)
TC_Renter_RentPark = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_RentPark)
TC_Renter_Edit_Profile = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_Edit_Profile)



test_suite = unittest.TestSuite([TC_Renter_FindParkNav, TC_Renter_RentPark, TC_Renter_Edit_Profile])

unittest.TextTestRunner().run(test_suite)
