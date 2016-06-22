"""
Process firmsrepresented.pdf from San Diego County


pdf to tif: convert -density 300 -depth 8 firmsrepresented.pdf firmsrepresented.tif
tif to text: tesseract -psm 6 firmsrepresented.tif firmsrepresented
text to csv: python3 firmsrepresented.Pu

lobbyist: {
  name: string,
  firms: list
}

firm: {
   info: string
   more_info: string [optional]
}


"""
import json

lobbyists = []

def last_name(n):
    if ',' in n:
        return n.split(',')[0]
    elif '.' in n:
        return n.split('.')[0]
    else:
        return n


def get_lobbyist_names(file_path):
    with open(file_path, 'r') as f:
        next(f)
        names = list(map(lambda x: x.split('|')[0], f.read().split('\n')))
        return ",".join([last_name(n) for n in names]).lower()
    

lobbyist_names = get_lobbyist_names('./lobbyists.csv')


def is_lobbyist(text):
    name = last_name(text).lower()
    return (name in lobbyist_names)


def new_lobbyist():
    l = {}
    l['firms'] = []
    return l


def is_garbage(line):
    if ("ATTACHMENT B" in line 
        or
        "REGISTERED LOBBYISTS AND" in line
        or 
        "compiled by the Clerk" in line
        or
        "Lobbyists will try to inﬂuence" in line
        or 
        "Note:" in line
        or
        "Lobbyist Name Reg" in line):
        return True
    else:
        return False


def is_corp_info(x):
    is_digit = lambda x: x in ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
    try: 
        return (is_digit(x[0]) and is_digit(x[1])) 
    except:
        print('is_corp_info called with', x)
        raise


def record_lobbyist(lobbyist):
    if lobbyist != {}:
        lobbyists.append(lobbyist)


def is_blank_line(x):
    return x == ""


def save():
    with open('firmsrepresented.json', 'w') as f:
        f.write(json.dumps(lobbyists, indent=4))


def total_firms():
    return sum([len(x['firms']) for x in lobbyists])


# text: array of lines
# lobbyist: dictionary
def parser(text, lobbyist, prior_corp=False):
    if len(text) == 0:
        return None  # base case
    elif is_blank_line(text[0]):
        return parser(text[1:], lobbyist, prior_corp=prior_corp)  # ignore line
    elif is_lobbyist(text[0]):
        record_lobbyist(lobbyist)       # lobbyist record finished. record it.
        lobbyist = new_lobbyist()       # make new lobbyist dictionary
        lobbyist['name'] = text[0]      # add name to lobbyist
        return parser(text[1:], lobbyist)
    elif is_corp_info(text[0]):
        corp_info = {'info': text[0]}
        lobbyist['firms'].append(corp_info)
        return parser(text[1:], lobbyist, prior_corp=True)
    elif is_garbage(text[0]):
        return parser(text[1:], lobbyist, prior_corp=prior_corp) # ignore line 
    elif prior_corp:
        # add additional info
        lobbyist['firms'][len(lobbyist['firms']) - 1]['more_info'] = text[0]
        return parser(text[1:], lobbyist, prior_corp=True)
    else:
        return parser(text[1:], lobbyist)
    
if __name__ == '__main__':
    with open('firmsrepresented.txt', 'r') as f:
        parser(f.read().split('\n'), {})
        print('Recorded', len(lobbyists), 'lobbyists')
        print('Total firms:', total_firms())
        save()
