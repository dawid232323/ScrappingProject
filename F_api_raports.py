import csv
import os
import xlsxwriter
import pandas as pd
from litex.regon import REGONAPI
from openpyxl import load_workbook 


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
        self.deleted_company = []
        self.raport_types = ['BIR11OsFizycznaDzialalnoscCeidg', 'BIR11OsFizycznaDzialalnoscRolnicza', 'BIR11OsFizycznaDzialalnoscPozostala', 'BIR11OsFizycznaDzialalnoscSkreslonaDo20141108']
        self.api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
        self.api.login('c5edf702474f47e78ad5')
        self.control_number = 0
    
    def create_environment(self):
        os.chdir('/Users/dawidpylak/Documents/Data/F_test/')
        writer = pd.ExcelWriter('F_ceidg.xlsx', engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter('F_agriculture.xlsx', engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter('F_rest.xlsx', engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter('F_deleted.xlsx', engine='xlsxwriter')
        writer.save()
    
    def get_branch(self, regon, raport_number):
        try:
            root = self.api.full_report(regon, raport_number)
        except:
            print("exception occured")
        position = {}
        for element in root.getchildren():
            position[element.tag] = element.text
        return position

    def breake_for_writing(self):
        self.make_spreadshit(self.ceidg_company, 'F_ceidg.xlsx')
        self.ceidg_company.clear()
        self.make_spreadshit(self.agricultural_company, 'F_agriculture.xlsx')
        self.agricultural_company.clear()
        self.make_spreadshit(self.rest_company, 'F_rest.xlsx')
        self.rest_company.clear()
        self.make_spreadshit(self.deleted_company, 'F_deleted.xlsx')
        self.deleted_company.clear()

    def make_spreadshit(self, result, name):
        df = pd.DataFrame(result)
        writer = pd.ExcelWriter(name, engine='openpyxl', mode='a')
        writer.book = load_workbook(name)
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        reader = pd.read_excel(name)
        if self.control_number == 0:
            df.to_excel(writer, index=False, header=True, startrow=len(reader) + 1)
        else:
            df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
        writer.close()

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
                if row[20] == '1':
                    self.deleted_company.append(self.get_branch(row[0], self.raport_types[-1]))
                counter += 1
            else:
                self.breake_for_writing()
                self.api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
                self.api.login('c5edf702474f47e78ad5') 
        self.breake_for_writing()     

def __main__():
    arrays = Result_Arrays()
    arrays.create_environment()
    arrays.make_raport()

if __name__ == '__main__':
    __main__()