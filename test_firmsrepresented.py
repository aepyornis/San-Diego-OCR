import unittest
# import tempfile
# from unittest.mock import patch

from firmsrepresented import *

class Test_new_lobbyist(unittest.TestCase):
    
    def test_returns_correct_dict(self):
        
        lobbyist = new_lobbyist()

        self.assertEqual(lobbyist, {'firms': []})

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

class Test_record_lobbyists(unittest.TestCase):

    
    def test_appends(self):
        self.assertEqual(lobbyists, [])
        record_lobbyist({})
        self.assertEqual(lobbyists, [])
        record_lobbyist('a lobbyist')
        self.assertEqual(lobbyists, ['a lobbyist'])
        

class Test_is_blank_line(unittest.TestCase):

    def test_is_blank(self):
        self.assertTrue(is_blank_line(""))
        self.assertFalse(is_blank_line("SOMETHING"))

class Test_is_corp_info(unittest.TestCase):
    
    def test_yes(self):
        lines = [ 
            "562 Golden Door BOS, County AssessorIRecorderlClerk, Sheriff's Dept., 'ITC, DA",
            "974 Center on Policy Initiatives BOS, BOS Reps., DA, Assistant DA, CAO,",
            "22 some corp",
            "1009 Greater San Diego Board of Supervisors, AssessorfRecorderIClerk",
            "995 Golden Eagle Management. LLC All Possible County Ofﬁces, BOS, Sheriff's Dept., DA. Assessor!"
        ]
        for line in lines:
            self.assertTrue(is_corp_info(line))
        
    def test_no(self):
        lines = [
            "Hill, Christie",
            "REALTORS",
            "PHONE (619) 531-5500 FAX (619) 595-461",
            "__—_—___—__",
            "List compiled by the Clerk of the Board of Supervisors Monday, June 6, 2016"
        ]
        for line in lines:
            self.assertFalse(is_corp_info(line))

        
class Test_is_garbage(unittest.TestCase):
    
    def test_some_garbage(self):
        
        garbage = [
            "ATTACHMENT B",
            "REGISTERED LOBBYISTS AND FIRMS REPRESENTED",
            "List compiled by the Clerk of the Board of Supervisors Monday, June 6, 2016",
            "Lobbyist Name Reg # Firm Represented Elective County OfficeIOfﬁcial *",
            "Note: \" List of the name(s) of the Elective County Office(s)IOl‘t'ieial(s) the Lobbyists will try to inﬂuence Page I 7 of 18"
        ]

        for x in garbage:
            self.assertTrue(is_garbage(x))
    
    def test_not_garbage(self):
        ok = [
            "815 Walmart Stores BOS, Members of the Planning Commission, BOS Reps., Sheriffs",
            "Department, Director of Planning and Land Use, CAO, Asst., CAO",
            "Attorneys Association"
        ]

        for x in ok:
            self.assertFalse(is_garbage(x))


class Test_last_name(unittest.TestCase):

     def test_name_with_comma(self):
         n = "Custar, Kristin, B"
         self.assertEqual(last_name(n), "Custar")

     def test_name_with_period(self):
         n = "Milch. James S."
         self.assertEqual(last_name(n), "Milch")
        

if __name__ == '__main__':
    unittest.main()
