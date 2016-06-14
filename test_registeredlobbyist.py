import unittest
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
        

class Test_good_line(unittest.TestCase):

    def test_false_if_blank_or_new_line(self):
        self.assertEqual(good_line(''), False)
        self.assertEqual(good_line('\n'), False)


if __name__ == '__main__':
    unittest.main()
