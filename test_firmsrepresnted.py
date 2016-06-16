import unittest
import tempfile
from unittest.mock import patch
import firmsrepresented
from firmsrepresented import *

class Test_start_line(unittest.TestCase):
    
    def test_is_start_line(self):
        line = "Lobbyist Name Reg # Firm Represented Elective County OfﬁceIOfﬁcial *"
        self.assertTrue(start_line(line))
    
    def test_is_not_start_line(self):
        line1 = "DAVID HALL. COB CLERK OF THE BOARD OF SUPERVISORS ANDREW POTTER"
        line2 = "REGISTERED LOBBYISTS AND FIRMS REPRESENTED"

        self.assertFalse(start_line(line1))
        self.assertFalse(start_line(line2))


class Test_last_name(unittest.TestCase):

    def test_name_with_comma(self):
        n = "Custar, Kristin, B"
        self.assertEqual(last_name(n), "Custar")

    def test_name_with_period(self):
        n = "Milch. James S."
        self.assertEqual(last_name(n), "Milch")
        

class Test_is_lobbyist(unittest.TestCase):
    
    def test_lobbyists(self):
        names = [
            "Adams. Matthew John",
            "Custar, Kristin",
            "Milch, James S.",
            "Stream, Theodore"
        ]

        for n in names:
            self.assertTrue(is_lobbyist(n))

    def test_not_lobbyists(self):
        lines = [
            "Company-San Diego",
            "1010 CVC Capital Partners (US). Inc. San Diego County Employees Retirement System",
            "ATTACHMENT B",
            "Ron Harper"
        ]
        for l in lines:
            self.assertFalse(is_lobbyist(l))

    
class Test_lower_last_name(unittest.TestCase):

    def test_lower_last(self):
        names = [
             "Bowling, Dennis C.", 
             "Bowman-Styles, Molly", 
             "Cason. Elizabeth"
        ]
        
        self.assertEqual(lower_last_names(names), ["bowling", "bowman-styles", "cason"])
        


# class Test_is_name(unittest.TestCase):
#     """"""
#     def test_is_name(self):
#         names = [
#             "Bowling, Dennis C.", 
#             "Bowman-Styles. Molly", 
#             "Cason, Elizabeth",
#             "Falcon. Clarissa Reyes",
#             "Kilkenny, Kim J.",
#             "Bryant III, John R."
#         ]
        
#         for n in names:
#             self.assertTrue(is_name(n))

#     def test_is_not_name(self):
#         not_names = [
#             "Jones Engineering",
#             "1015 Barclays Capital, Inc. County Treasurer~Tax Collector",
#             "Management Ltd.",
#             "Park, LLC",
#             "dba Father Joe's Villages",
            
#         ]
    
    

if __name__ == '__main__':
    unittest.main()
