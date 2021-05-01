from litex.regon import REGONAPI
from lxml import etree
from lxml import objectify
import pandas as pd 
import xlsxwriter




raport_type = {'P':['BIR11OsPrawna', 'BIR11OsPrawnaPkd'] ,
'F':['BIR11OsFizycznaDaneOgolne', 'BIR11OsFizycznaPkd'] ,
'LF':['BIR11JednLokalnaOsFizycznej','BIR11JednLokalnaOsFizycznejPkd'],
 'LP':['BIR11JednLokalnaOsPrawnej','BIR11JednLokalnaOsPrawnejPkd']}


def open_file(rpt, num, inputName):
    with open(inputName) as fhand:
        for line in fhand:
            if line.startswith(rpt):
                print('starts with ', rpt)
                line = line.rstrip('\n').split()
                type = raport_type[line[0]][num]
                regon = line[1]
                print('got ', type, regon)
                yield type, regon

def common_raport(rpt, num, api, result, inputName):
    for type, regon in open_file(rpt, num, inputName):
        try:
            root = api.full_report(regon, type)
        except:
            break
        position = {}
        for elem in root.getchildren():
            position[elem.tag] = elem.text
        result.append(position)
        del(position)
    

def pkd_raport(rpt, num, api, result, inputName):
    for type, regon in open_file(rpt, num, inputName):
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

def get_raport(rpt, num, inputName):
    result = []
    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
    api.login('c5edf702474f47e78ad5')
    if num == 0:
        common_raport(rpt, num, api, result, inputName)
    elif num == 1:
        pkd_raport(rpt, num, api, result, inputName)
    return result


def make_spreedsheet(result, name):
    df = pd.DataFrame(result)
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1')
    writer.save()

if __name__ == '__main__':
    rp = input('specify company type ("P", "F" etc.) ')
    num = int(input('Specify rapot type - 0 for common, 1 for pkd '))
    inputName = input('specify input name ("d" for default settings) ')
    if inputName == 'd':
        make_spreedsheet(get_raport(rp, num, 'regons.txt'), 'raport_output.xlsx')
    else:  
        outputName = input('specify output name ')
        make_spreedsheet(get_raport(rp, num, inputName), outputName)
