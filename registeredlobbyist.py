"""
Process the registeredlobbyist file from San Diego County.

pdf to tif: convert -density 300 -depth 8 registeredlobbyist.pdf lobbyist.tif
tif to text:  tesseract -psm 4 lobbyist.tif lobbyist

note: at this step you *may* have to manually fix one or two names 
      if errors occur with the python script.

text to csv: python3 registeredlobbyist.py 
outputs: lobbyists.csv
"""
import re

FILE_PATH = 'lobbyist.txt'

OUT_FILE = 'lobbyists.csv'

LOBBYIST_LINE_PATTERN = """
^              # beginning of string
.+             # anything
[,.]           # comma or a period
[ ]+           # space 
.+             # anything  
[0-9l\]\[]{2,3} # 2-4 digital number or bracket, sometimes 1 becomes a []
[ ]            # space
.+             # anything
$              # end
"""
lobbyist_re = re.compile(LOBBYIST_LINE_PATTERN, re.I|re.X)

LOBBYIST_GROUPS_PATTERN = """
^              # beginning of string
(.+)           # Name = Group1
[ ]+           # space
([0-9l]{3,})   # reg = Group2. numbers or 'l'
[ ]+           # space
(.+)           # targets = group3
$              # end

"""

lobbyist_groups_re = re.compile(LOBBYIST_GROUPS_PATTERN, re.I|re.X)


def write_headers():
    with open(OUT_FILE, 'w') as f:
        f.write('name|reg|officials')
        f.write('\n')

def start_line(l):
    """
    Returns true if line contains "Lobbyist" and "Registrant" and "Name" and "reg"
    """
    if (
            re.search("Lobbyist", l, flags=re.I) and 
            re.search("Registrant", l, flags=re.I) and
            re.search("Name", l, flags=re.I) and
            re.search("reg", l, flags=re.I)
    ):
        return True
    else:
        return False
    


def good_line(l):
    if lobbyist_re.search(l) is None:
        return False
    else:
        return True


def good_line_to_csv(l):
    """
    Turns brackets into ], [ => 1 and then line into csv (using |)
    replace l with 1 in reg number
    """
    line_with_fixed_brackets = l.replace('[', '1').replace(']', '1')

    m = lobbyist_groups_re.match(line_with_fixed_brackets)
    if m:
        return m.group(1) + "|" + m.group(2).replace('l', '1') + "|" + m.group(3)
    else:
        raise Exception("No match with: " + l)



def process_line(l):
    with open(OUT_FILE, 'a') as f:
        f.write(good_line_to_csv(l))
        f.write('\n')


def line_loop(f):
    """ Flow:
    empty string -> end of file.
    good line and next line is blank ->  process line
    good line and the next line is not blank -> concat the two lines and then process.
    else -> skip the line
    """
    while True:
        line = f.readline()
        if line == "":
            break
        elif good_line(line):
            following_line = f.readline()
            if following_line != '\n':
                process_line((line + " " + following_line).replace('\n',''))
            else:
                process_line(line.replace('\n', ''))
        else:
            pass
                
def main():
    write_headers()
    with open(FILE_PATH, 'r') as f:
        for line in f:
            if start_line(line):
                break
            else:
                pass
        line_loop(f)

if __name__ == '__main__':
    main()
