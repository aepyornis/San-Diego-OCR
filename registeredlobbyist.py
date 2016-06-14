"""
Process the registeredlobbyist file from San Diego County.

pdf to tif: convert -density 300 -depth 8 registeredlobbyist.pdf lobbyist.
tif to text:  tesseract -psm 4 lobbyist.tif lobbyist
text to csv: python3 registeredlobbyist.py > registeredlobbyist.csv

"""
import re
# import csv

FILE_PATH = 'lobbyist.txt'

LOBBYIST_LINE_PATTERN = """
^              # beginning of string
.+             # anything
[,]            # comma
.+             # anything  
[0-9\]\[]{2,3} # 2-4 digital number or bracket, sometimes 1 becomes a []
[ ]            # space
.+             # anything
$              # end
"""

lobbyist_re = re.compile(LOBBYIST_LINE_PATTERN, re.I|re.X)

def good_line(l):
    if lobbyist_re.search(l) is None:
        return False
    else:
        return True


def main():
    with open(FILE_PATH, 'r') as f:
        for line in f:
            if good_line(line):
                pass

if __name__ == '__main__':
             main()
