from litex.regon import REGONAPI
from lxml import etree
from lxml import objectify
import pandas as pd 
import xlsxwriter


def file_handle():
    with open('nips.txt') as file:
        for line in file:
            line = line.rstrip('\n')
            yield line

def get_search_results():
    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
    api.login('c5edf702474f47e78ad5')
    for item in file_handle():
        try:
            root = api.search(nip=item)
        except Exception as ex:
            print(ex)
            op = input('continue? ')
            if op == 'y':
                continue
            else:
                break
        for elem in root:
            yield elem.Typ.text, elem.Regon.text

def write_to_file():
    file = open('regon.txt','w')
    for type, regon in get_search_results():
        res = type + ' ' + regon + '\n'
        print('writing ', res)
        file.write(res)
    file.close()

if __name__ == '__main__':
    
    write_to_file()