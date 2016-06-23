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
             "Stream, Theodore",
             "Addis-Mills, A"
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
        

class Test_split_info(unittest.TestCase):
    
    def test_extracts_name(self):
        self.assertEqual(
            split_info("784 Bearing Point County Treasurer-Tax Collector")[1],
            "Bearing Point County"
        )
        self.assertEqual(
            split_info("786 Mary McGuire Board of Supervisors, PDS")[1],
            "Mary McGuire"
        )
        
        self.assertEqual(
            split_info("866 Paci\ufb01ca Enterprises, Inc. BOS, BOS Reps., BOS Staff, CAO & Directors of Planning &")[1],
            "Paci\ufb01ca Enterprises, Inc."
        )

    def test_extract_num(self):
        self.assertEqual(
            split_info("784 Bearing Point County Treasurer-Tax Collector")[0],
            "784")
        self.assertEqual(
            split_info("786 Mary McGuire Board of Supervisors, PDS")[0],
            "786")
        
        self.assertEqual(
            split_info("866 Paci\ufb01ca Enterprises, Inc. BOS, BOS Reps., BOS Staff, CAO & Directors of Planning &")[0],
            "866")
        

    # def test_extracts_targets

    def test_extract_num(self):
        self.assertEqual(
            split_info("784 Bearing Point County Treasurer-Tax Collector")[2],
            "Treasurer-Tax Collector")
        self.assertEqual(
            split_info("786 Mary McGuire Board of Supervisors, PDS")[2],
            "Board of Supervisors, PDS")
        
        self.assertEqual(
            split_info("866 Paci\ufb01ca Enterprises, Inc. BOS, BOS Reps., BOS Staff, CAO & Directors of Planning &")[2],
            "BOS, BOS Reps., BOS Staff, CAO & Directors of Planning &")
    

    def test_raises_excpetion_when_no_target_found(self):
        with self.assertRaises(Exception):
            split_info('666 the devil, inc. god')


class Test_add_num_corp_name_targets_to_lobbyist(unittest.TestCase):
    john = {"name": "Alexander. John Scott","firms": [{"info": "1006 Statue of Responsibility Board of Supervisors, Treasurer-Tax Collector"}]}

    def test_adds_num(self):
        result = add_num_corp_name_targets_to_lobbyist(self.john)
        self.assertEqual(result['firms'][0]['number'], "1006")
        
    def test_adds_corp_name(self):
        result = add_num_corp_name_targets_to_lobbyist(self.john)
        self.assertEqual(result['firms'][0]['corp_name'], "Statue of Responsibility")

    def test_adds_targets(self):
        result = add_num_corp_name_targets_to_lobbyist(self.john)
        self.assertEqual(result['firms'][0]['targets'], "Board of Supervisors, Treasurer-Tax Collector")
        
    
class Test_process_more_info(unittest.TestCase):
    f = {'number': '1006', 'info': '1006 Statue of Responsibility Board of Supervisors, Treasurer-Tax Collector', 'targets': 'Board of Supervisors, Treasurer-Tax Collector', 'corp_name': 'Statue of Responsibility'}
        

    def test_returns_firm_if_no_more_info(self):
        self.assertEqual(process_more_info(self.f), self.f)
        
    def test_more_info_is_part_of_corp_name(self):
        firm = {'number': '1', 'targets': 'Board of Supervisors', 'corp_name': 'Mega Corp', 'info': '1 Mega Corp Board of Supervisors', 'more_info': 'INC'}
        self.assertEqual(process_more_info(firm)['corp_name'], 'Mega Corp INC')

    def test_more_info_is_part_of_targets(self):
        firm = {'number': '1', 'targets': 'Board of Supervisors', 'corp_name': 'Mega Corp', 'info': '1 Mega Corp Board of Supervisors', 'more_info': 'BOS'}
        _f = process_more_info(firm)
        self.assertEqual(_f['corp_name'], 'Mega Corp')
        self.assertEqual(_f['targets'], 'Board of Supervisors BOS')

    def test_more_info_is_part_of_corp_name_2(self):
        firm ={
                "info": "507 San Diego County All Possible County",
                "corp_name": "San Diego County",
                "number": "507",
                "targets": "All Possible County",
                "more_info": "Apartment Association"
        }
        self.assertEqual(firm['corp_name'], "San Diego County")
        firm = process_more_info(firm)
        self.assertEqual(firm['corp_name'], "San Diego County Apartment Association")
        

    def test_more_info_contains_both(self):
        firm = {'number': '1', 'targets': 'Board of Supervisors', 'corp_name': 'Mega Corp', 'info': '1 Mega Corp Board of Supervisors', 'more_info':'INC BOS'}
        _f = process_more_info(firm)
        self.assertEqual(_f['corp_name'], 'Mega Corp INC')
        self.assertEqual(_f['targets'], 'Board of Supervisors BOS')


class Test_csv_pipe_warning(unittest.TestCase):
    def test_raises(self):
        with self.assertRaises(Exception):
            csv_pipe_warning('blahblah|blah')


if __name__ == '__main__':
    unittest.main()
 
