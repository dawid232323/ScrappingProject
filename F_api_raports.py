import csv
import pandas as pd
from litex.regon import REGONAPI


class file_handler():
    def __init__(self):
        self.fhand = open('/Users/dawidpylak/Documents/Data/F_test/test.csv', encoding="utf8", mode='r')
        self.csv_reader = csv.reader(self.fhand, delimiter=';')
    def get_file(self):
        names = next(self.csv_reader)
        for row in self.csv_reader:
            yield row

class Result_Arrays():
    def __init__(self):
        self.ceidg_company = []
        self.agricultural_company = []
        self.rest_company = []
        self.raport_types = ['BIR11OsFizycznaDzialalnoscCeidg', 'BIR11OsFizycznaDzialalnoscRolnicza', 'BIR11OsFizycznaDzialalnoscPozostala']
        self.api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
        self.api.login('c5edf702474f47e78ad5')
    def get_branch(self, regon, raport_number):
        try:
            root = self.api.full_report(regon, raport_number)
        except:
            print("exception occured")
        position = {}
        for element in root.getchildren():
            position[element.tag] = element.text
        return position

    def make_spreadshit(self):
        print('ceidg: ', self.ceidg_company,'agricultural ', self.agricultural_company, 'rest ', self.rest_company, sep='\n')

    def make_raport(self):
        counter = 0
        for row in file_handler().get_file():
            if counter < 1660:
                if row[17] == '1':
                    self.ceidg_company.append(self.get_branch(row[0], self.raport_types[0]))
                if row[18] == '1':
                    self.agricultural_company.append(self.get_branch(row[0], self.raport_types[1]))
                if row[19] == '1':
                    self.rest_company.append(self.get_branch(row[0], self.raport_types[2]))
                counter += 1
            else:
                self.make_spreadshit()
                self.api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
                self.api.login('c5edf702474f47e78ad5') 
        self.make_spreadshit()               

def __main__():
    arrays = Result_Arrays()
    arrays.make_raport()

if __name__ == '__main__':
    __main__()