import unittest
from SeleniumTestScripts.TC_Renter_SuccessfulLogin import TC_Renter_SuccessfulLogin
from SeleniumTestScripts.TC_Renter_UnsuccessfulLogin import TC_Renter_UnsuccessfulLogin
from SeleniumTestScripts.TC_Renter_Sign_up import TC_Renter_Sign_up

TC_Renter_Sign_up = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_Sign_up)
TC_Renter_SuccessfulLogin = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_SuccessfulLogin)
TC_Renter_UnsuccessfulLogin = unittest.TestLoader().loadTestsFromTestCase(TC_Renter_UnsuccessfulLogin)


test_suite = unittest.TestSuite([TC_Renter_SuccessfulLogin, TC_Renter_UnsuccessfulLogin, TC_Renter_Sign_up])

unittest.TextTestRunner().run(test_suite)
