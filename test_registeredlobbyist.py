import unittest
import tempfile

from unittest.mock import patch
import registeredlobbyist
from registeredlobbyist import *

class Test_lobbyist_re(unittest.TestCase):

    def test_sample_lobbyist_lines(self):
        line1 = "Harris, Sondra M. 668 Board of Supervisors, DPLU, BPZA, PERB, CAO, Asst. CAO, Board Reps."
        line2 = "Rupp III, Henry 788 BOS & Staff, PDS & Staff, Planning Commission & Staff, DPW Staff, CAO"
        line3 = "Silverman, Stephen [-1. 776 Board of Supervisors, Planning Comm, PDS"
        line4 = "Rosenbaum, S. Wayne 92] BOS, Members of Planning Commission, BOS Representatives & PDS"
        
        self.assertIsNotNone(lobbyist_re.search(line1))
        self.assertIsNotNone(lobbyist_re.search(line2))
        self.assertIsNotNone(lobbyist_re.search(line3))
        self.assertIsNotNone(lobbyist_re.search(line4))
        
    def test_non_lobbyist_lines(self):
        line1 = "Note: * List of the name(s) of the Elective County 0fﬂce(s)/Oﬂicial(s) the Lobbyists will try to inﬂuence Page 5 of 6"
        line2 = "List compiled by the Clerk of the Board of Supervisors Monday, June 6, 2016"
        line3 = "PHONE (519) 531-5500 FAX (51915954515"
        
        self.assertIsNone(lobbyist_re.search(line1))
        self.assertIsNone(lobbyist_re.search(line2))
        self.assertIsNone(lobbyist_re.search(line3))
        



class Test_lobbyist_groups_re(unittest.TestCase):
    
    def test_line1(self):
        line = "Harris, Sondra M. 668 Board of Supervisors, DPLU, BPZA, PERB, CAO, Asst. CAO, Board Reps."
        m = lobbyist_groups_re.match(line)
        
        self.assertEqual(m.group(1), "Harris, Sondra M.")
        self.assertEqual(m.group(2), "668")
        self.assertEqual(m.group(3), "Board of Supervisors, DPLU, BPZA, PERB, CAO, Asst. CAO, Board Reps.")
        

    def test_line2(self):
        line = "Reilly, James 1016 County Treasurer—Tax Collector"
        m = lobbyist_groups_re.match(line)

        self.assertEqual(m.group(1), "Reilly, James")
        self.assertEqual(m.group(2), "1016")
        self.assertEqual(m.group(3), "County Treasurer—Tax Collector")

    def test_line3_catches_l_in_reg(self):
        line = "Capretz, Nicole l012 Board of Supervisors"
        m = lobbyist_groups_re.match(line)
        
        self.assertEqual(m.group(1), "Capretz, Nicole")
        self.assertEqual(m.group(2), "l012")
        self.assertEqual(m.group(3), "Board of Supervisors")
        
            
class Test_good_line_to_csv(unittest.TestCase):
    
    def test_line_without_brackets(self):
        line = "Reilly, James 1016 County Treasurer—Tax Collector"
        csv = good_line_to_csv(line)
        self.assertEqual(csv, "Reilly, James|1016|County Treasurer—Tax Collector")

    def test_line_with_brackets(self):
        line = "Reilly, James [0]6 County Treasurer—Tax Collector"
        csv = good_line_to_csv(line)
        self.assertEqual(csv, "Reilly, James|1016|County Treasurer—Tax Collector")

class Test_good_line(unittest.TestCase):

    def test_false_if_blank_or_new_line(self):
        self.assertEqual(good_line(''), False)
        self.assertEqual(good_line('\n'), False)


    def test_good_line(self):
        line1 = "Harris, Sondra M. 668 Board of Supervisors, DPLU, BPZA, PERB, CAO, Asst. CAO, Board Reps."
        self.assertTrue(good_line(line1))


class Test_line_loop(unittest.TestCase):

    @patch.object(registeredlobbyist, 'process_line')
    def test_end_of_file(self, mock):
        with tempfile.TemporaryFile(mode='r') as fp:
            line_loop(fp)
            self.assertFalse(mock.called)

    @patch.object(registeredlobbyist, 'process_line')
    def test_good_line_followed_by_blank(self, mock):
        
        with tempfile.TemporaryFile(mode='w+') as fp:
            
            fp.write("Whalen, James E. 736 Board of Supervisors, Director of PDS, BOS Reps., Planning Comm, Deputy CAO")
            fp.write("\n")
            fp.seek(0)
            
            line_loop(fp)
            self.assertTrue(mock.called)

    @patch.object(registeredlobbyist, 'process_line')
    def test_good_line_followed_by_more_info(self, mock):
        
        with tempfile.TemporaryFile(mode='w+') as fp:
            
            fp.write("Whalen, James 736 Board of Supervisors\n")
            fp.write("HHSA")
            fp.write("\n")
            fp.seek(0)
            line_loop(fp)
            self.assertTrue(mock.called)
            self.assertEqual(mock.call_args[0][0], "Whalen, James 736 Board of Supervisors HHSA")


class Test_start_line(unittest.TestCase):
    
    def test_is_start_line(self):
        line = "Lobbyist/Registrant Name Reg # Elective County Office/Ofﬁcial *"
        self.assertTrue(start_line(line))

    def test_is_not_start_line(self):
        lines = [
            "DAVID HALL. CCB CLERK OF THE BOARD OF SUPERVISORS ANDREW POTTER",
            "EXECUT'VE mam Isoo PACIFIC HIGHWAY. ROOM 402. SAN DIEGO. CALIFORNIA 92101-2471",
            "Ernest J. Dronenburg J r., Assessor/RecorderlCounty Clerk",
            "lobbyist and the elective ofﬁces/officials that the lobbyists will attempt to inﬂuence.",
            "SAN DIEGO COUNTY REGISTERED LOBBYISTS"
        ]
        
        for l in lines:
            self.assertFalse(start_line(l))
        
    
if __name__ == '__main__':
    unittest.main()
