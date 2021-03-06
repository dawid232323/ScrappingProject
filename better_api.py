from litex.regon import REGONAPI
from lxml import etree
from lxml import objectify
import pandas as pd 
import xlsxwriter
import csv
import re
import os 
from openpyxl import load_workbook 

raport_type = {'P':['BIR11OsPrawna', 'BIR11OsPrawnaPkd'] ,
'F':['BIR11OsFizycznaDaneOgolne', 'BIR11OsFizycznaPkd'] ,
'LF':['BIR11JednLokalnaOsFizycznej','BIR11JednLokalnaOsFizycznejPkd'],
 'LP':['BIR11JednLokalnaOsPrawnej','BIR11JednLokalnaOsPrawnejPkd']}

class file_handler():
    def __init__(self):
        self.input_name = 'temp'
        self.output_name = "temp.xlsx"
        self.lines = None

    def open_file(self):
        self.input_name = '/home/dawid232323/Documents/PKD/to_do/'+ self.output_name + '.xlsx'
        file = pd.read_excel(self.input_name, dtype={'regon':str, 'type':str, 'name':str,
        'Województwo':str, 'Powiat': str, 'Gmina':str, 'Kod Pocztowy': str, 'Miasto': str, 'Ulica':str,
        'Informacja o usuniętym wpisie':str})
        # print(file)
        return file
    
    def open_list_file(self):
        ls_file = open("list_of_counties.txt", 'r' , encoding='UTF-8')
        self.lines = ls_file.readlines()
        # print(lines)
        self.output_name = re.sub('.xlsx', '', self.lines[0].rstrip('\n'))
        print('output name is ', self.output_name)
        ls_file.close()
        ls_file = open("list_of_counties.txt", 'w' , encoding='UTF-8')
        ls_file.truncate()
        ls_file.writelines(self.lines[1:])
        ls_file.close()
    
    

class Result_Arrays():
    

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.file = self.file_handler.open_file()
        self.common_P_result = []
        self.pkd_P_result = []
        self.common_F_result = []
        self.pkd_F_result = []
        self.common_LF_result = []
        self.pkd_LF_result = []
        self.common_LP_result = []
        self.pkd_LP_result = []
        self.common_P_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_P.csv'
        self.common_F_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_F.csv'
        self.common_LF_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_LF.csv'
        self.common_LP_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_LP.csv'
        self.pkd_F_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_F.csv'
        self.pkd_P_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_P.csv'
        self.pkd_LP_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_LP.csv'
        self.pkd_LF_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_LF.csv'
        self.control_number = 0

    def create_environment(self):
        os.mkdir(f'/home/dawid232323/Documents/PKD/done/{self.file_handler.output_name}')
        os.chdir(f'/home/dawid232323/Documents/PKD/done/{self.file_handler.output_name}')
        # writer = pd.ExcelWriter(self.common_P_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.common_F_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.common_LP_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.common_LF_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.pkd_P_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.pkd_F_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.pkd_LP_name, engine='xlsxwriter')
        # writer.save()
        # writer = pd.ExcelWriter(self.pkd_LF_name, engine='xlsxwriter')
        # writer.save()

    def common_raport(self, api, regon, result, cmp_type):
        try:
            root = api.full_report(regon, cmp_type)
        except:
            print('przy raporcie common',Exception)
        position = {}
        for elem in root.getchildren():
            position[elem.tag] = elem.text
        result.append(position)
        del(position)

    def pkd_raport(self, api, result, regon, cmp_type):
        try:
            root = api.full_report(regon, cmp_type)
        except:
            print('przy raporcie pkd',Exception)
        for branch in root:
            position = {}
            for element in branch.getchildren():
                position['regon'] = regon
                position[element.tag] = element.text
            result.append(position)
            del(position)

    def make_spreedsheet(self, result, name):
        df = pd.DataFrame(result)
        if self.control_number == 0:
            df.to_csv(name, mode='a', sep=';', index=False, header=True, encoding='UTF-8')
        else:
            df.to_csv(name, mode='a', sep=';', index=False, header=False, encoding='UTF-8')
        
    def convert_to_excel(self):
        file_list = os.listdir('.')
        for file_name in file_list:
            print('converting ', file_name)
            file_to_convert = open(file_name, encoding='UTF-8')
            reader = csv.reader(file_to_convert, delimiter=';')
            file_name = file_name.replace('.csv', '.xlsx')
            read = pd.DataFrame(reader)
            # writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            # writer.save()
            read.to_excel(file_name, header=True, index=False)
    def delete_csv(self):
        for file_name in os.listdir():
            if file_name.endswith('.csv'):
                os.remove(file_name)

    def emergency_break(self):
        self.make_spreedsheet(self.common_P_result, self.common_P_name)
        self.make_spreedsheet(self.common_F_result, self.common_F_name)
        self.make_spreedsheet(self.common_LF_result, self.common_LF_name)
        self.make_spreedsheet(self.common_LP_result, self.common_LP_name)
        self.make_spreedsheet(self.pkd_P_result, self.pkd_P_name)
        self.make_spreedsheet(self.pkd_F_result, self.pkd_F_name)
        self.make_spreedsheet(self.pkd_LF_result, self.pkd_LF_name)
        self.make_spreedsheet(self.pkd_LP_result, self.pkd_LP_name)
        self.common_F_result.clear()
        self.common_LF_result.clear()
        self.common_LP_result.clear()
        self.common_P_result.clear()
        self.pkd_F_result.clear()
        self.pkd_LF_result.clear()
        self.pkd_LP_result.clear()
        self.pkd_P_result.clear()
        self.control_number = 1

    def raport_type(self, argument, api):
        if argument['type'] == 'P':
            self.pkd_raport(api, self.pkd_P_result, argument['regon'], raport_type['P'][1])    
            self.common_raport(api, argument['regon'], self.common_P_result, raport_type['P'][0])
        elif argument['type'] == 'F':
            self.pkd_raport(api, self.pkd_F_result, argument['regon'], raport_type['F'][1])    
            self.common_raport(api, argument['regon'], self.common_F_result, raport_type['F'][0])
        elif argument['type'] == 'LF':
            self.pkd_raport(api, self.pkd_LF_result, argument['regon'], raport_type['LF'][1])    
            self.common_raport(api, argument['regon'], self.common_LF_result, raport_type['LF'][0])
        elif argument['type'] == 'LP':
            self.pkd_raport(api, self.pkd_LP_result, argument['regon'], raport_type['LP'][1])    
            self.common_raport(api, argument['regon'], self.common_LP_result, raport_type['LP'][0])
        else:
            print('type not found')

    def get_raport(self):
        counter = 0
        self.file_handler.output_name = 1
        api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
        api.login('c5edf702474f47e78ad5')
        for row in self.file.iterrows():
            if counter < 2500:
                try:
                    self.raport_type(row[1], api)
                    counter += 1  
                    print('Done ', row[1]['regon'] ,row[1]['name'])
                except KeyboardInterrupt:
                    self.emergency_break()
                    exit()
                
                except Exception as e:
                    print('first if ', e)
                    counter += 1  
                    continue
                
            else:
                try:
                    self.emergency_break()
                    print('file written')
                except:
                    print('emergency ', Exception)
                counter = 0
                try:
                    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
                    api.login('c5edf702474f47e78ad5')
                except:
                    print('api ', Exception)
        self.emergency_break()

if __name__ == '__main__':
    file_handler = file_handler()
    file_handler.open_list_file()
    arrays = Result_Arrays(file_handler)
    arrays.create_environment()
    arrays.get_raport()
    arrays.convert_to_excel()
    arrays.delete_csv()





