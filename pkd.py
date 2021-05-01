from litex.regon import REGONAPI
from lxml import etree
from lxml import objectify
import pandas as pd 
import xlsxwriter

# api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
# api.login('c5edf702474f47e78ad5')
# root = api.full_report('431017745', 'BIR11OsPrawna')


raport_type = {'P':'BIR11OsPrawnaPkd' ,'F':'BIR11OsFizycznaPkd' ,'LF':'BIR11JednLokalnaOsFizycznej',
 'LP':'BIR11JednLokalnaOsPrawnej'}


def open_file(rpt):
    with open('regon_test.txt') as fhand:
        for line in fhand:
            if line.startswith(rpt):
                print('starts with ', rpt)
                line = line.rstrip('\n').split()
                type = raport_type[line[0]]
                regon = line[1]
                print('got ', type, regon)
                yield type, regon

def get_raport(rpt):
    result = []
    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
    api.login('c5edf702474f47e78ad5')
    for type, regon in open_file(rpt):
        try:
            root = api.full_report(regon, type)
        except:
            break
        for branch in root:
            position = {}
            for element in branch.getchildren():
                position['regon'] = regon
                position[element.tag] = element.text
            result.append(position)
            del(position)
        
    return result


def make_spreedsheet(result, name):
    df = pd.DataFrame(result)
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1')
    writer.save()

if __name__ == '__main__':
    rp = input('specify company type ')
    outputName = input('specify output name ')
    make_spreedsheet(get_raport(rp), outputName)
