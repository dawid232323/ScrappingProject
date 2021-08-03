import csv
import os
import xlsxwriter
import pandas as pd
from litex.regon import REGONAPI
from openpyxl import load_workbook 


class file_handler():
    def __init__(self):
        self.fhand = open('/home/dawid232323/Documents/F raports/common_f.csv', encoding="utf8", mode='r')
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
        os.chdir('/home/dawid232323/Documents/F raports/')
        # writer = pd.ExcelWriter('F_ceidg.xlsx', engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter('F_agriculture.xlsx', engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter('F_rest.xlsx', engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter('F_deleted.xlsx', engine='xlsxwriter')
        # writer.save()
        # print('Created files')
    
    def get_branch(self, regon, raport_number):
        try:
            root = self.api.full_report(regon, raport_number)
        except:
            print("Exception occured")
        position = {}
        for element in root.getchildren():
            position[element.tag] = element.text
        return position

    def breake_for_writing(self):
        self.make_spreadshit(self.ceidg_company, 'F_ceidg.csv')
        self.ceidg_company.clear()
        self.make_spreadshit(self.agricultural_company, 'F_agriculture.csv')
        self.agricultural_company.clear()
        self.make_spreadshit(self.rest_company, 'F_rest.csv')
        self.rest_company.clear()
        self.make_spreadshit(self.deleted_company, 'F_deleted.csv')
        self.deleted_company.clear()
        print('File written')
        self.control_number = 1

    def make_spreadshit(self, result, name):
        df = pd.DataFrame(result)
        if self.control_number == 0:
            df.to_csv(name, mode='a', header=True, index=False, sep=';')
        else:
            df.to_csv(name, mode='a', header=False, index=False, sep=';')
        

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
                print('Done', row[0])
                counter += 1
            else:
                print('starting else')
                counter = 0
                self.breake_for_writing()
                self.api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
                self.api.login('c5edf702474f47e78ad5') 
                print('zeroed counter')
        self.breake_for_writing()     

def __main__():
    arrays = Result_Arrays()
    arrays.create_environment()
    try:
        arrays.make_raport()
    except Exception:
        # print('keyboard interrupt')
        arrays.breake_for_writing()
        exit()  

if __name__ == '__main__':
    __main__() 