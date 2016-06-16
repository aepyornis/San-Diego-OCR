"""
Process the firmsepresented file from San Diego County

pdf to tif: convert -density 300 -depth 8 firmsrepresented.pdf firmsrepresented.tif
tif to text: tessaract -psm 6 firmsrepresented.tif firmsrepresented
text to csv: python3 firmsrepresented.py
"""
import re

FILE_PATH = './firmsrepresented/firmsrepresented_6.txt'
OUT_FILE = 'firmsrepresented.csv'


def lobbyists(fp):
    """Returns names of lobbyists from file"""
    names = []
    with open(fp, 'r') as f:
        next(f)  # skip header
        for line in f:
             names.append(line.split('|')[0])
    return names
    

def start_line(l):
    """
    Returns true if the the line starts with "Lobbyist Name"
    """
    regex = r"^Lobbyist Name.+"
    return (re.match(regex, l, flags=re.I) is not None)

def end_line(l):
    """
    Note: " List of the name(s) of the Elective County Office(s)IOl‘t'ieial(s) the Lobbyists will try to inﬂuence Page I 7 of 18
    """
    pass

def last_name(name):
    if 
    try:
        return name[0:name.index(',')]
    except ValueError:
         return name[0:name.index('.')]
    except ValueError:
        return ''


def lower_last_names(names):
    """
    list of names -> list of last names lowerccased
    """
    return list(map(lambda x: last_name(x.lower()),names))

LOBBYISTS = lobbyists('./lobbyists.csv')
def is_lobbyist(name):
    names = lower_last_names(LOBBYISTS)
    
    if len([x for x in names if last_name(name).lower() in names]) > 0:
        return True
    else:
        return False


def is_name(l):
    """
    Returns true if the line is a lobbyist's name
    """
    pass


def line_loop(f):
    """
    General detection pattern:
    
    Is Lobbyist ->
       record lobbyist info
       Next line ->
           if firm represtned?
               record.
                next line ->
                  is another firm?
                     reocrd, continue
                  is not a lobbyist?
                     append info to firm represtened
                  is page divider?
                     skip
                  is lobbyist?
                      done.
    """
    while True:
        line = f.readline()
        if line == "":
            break
        elif is_lobbyist(l):
            pass
        else:
            pass


def main():
    with open(FILE_PATH, 'r') as f:
        for line in f:
            if start_line(line):
                break
            else:
                pass

        line_loop(f)

if __name__ == '__main__':
    main()                      
    # lobbyists('./lobbyists.csv') 

