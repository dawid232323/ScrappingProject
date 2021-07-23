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

    def open_file(self):
        self.input_name = self.output_name + '.xlsx'
        file = pd.read_excel(self.input_name, index_col=0, dtype={'Regon':str, 'Typ':str, 'Nazwa':str,
        'Województwo':str, 'Powiat': str, 'Gmina':str, 'Kod Pocztowy': str, 'Miasto': str, 'Ulica':str,
        'Informacja o usuniętym wpisie':str})
        # print(file)
        return file
    
    def open_list_file(self):
        ls_file = open("list_of_counties.txt", 'r' , encoding='UTF-8')
        lines = ls_file.readlines()
        # print(lines)
        self.output_name = re.sub('.xlsx', '', lines[0].rstrip('\n'))
        print('output name is ', self.output_name)
        ls_file.close()
        ls_file = open("list_of_counties.txt", 'w' , encoding='UTF-8')
        ls_file.truncate()
        ls_file.writelines(lines[1:])
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
        self.common_P_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_P.xlsx'
        self.common_F_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_F.xlsx'
        self.common_LF_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_LF.xlsx'
        self.common_LP_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_common_LP.xlsx'
        self.pkd_F_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_F.xlsx'
        self.pkd_P_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_P.xlsx'
        self.pkd_LP_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_LP.xlsx'
        self.pkd_LF_name = re.sub('.xlsx', '', self.file_handler.output_name) + '_pkd_LF.xlsx'
        self.control_number = 0

    def create_environment(self):
        os.mkdir(f'/Users/dawidpylak/Dysk Google/REGON/2_comp_general/{self.file_handler.output_name}')
        os.chdir(f'/Users/dawidpylak/Dysk Google/REGON/2_comp_general/{self.file_handler.output_name}')
        writer = pd.ExcelWriter(self.common_P_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.common_F_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.common_LP_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.common_LF_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.pkd_P_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.pkd_F_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.pkd_LP_name, engine='xlsxwriter')
        writer.save()
        writer = pd.ExcelWriter(self.pkd_LF_name, engine='xlsxwriter')
        writer.save()

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
        writer = pd.ExcelWriter(name, engine='openpyxl', mode='a')
        writer.book = load_workbook(name)
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        reader = pd.read_excel(name)
        if self.control_number == 0:
            df.to_excel(writer, index=False, header=True, startrow=len(reader) + 1)
        else:
            df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
        writer.close()

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
        if argument['Typ'] == 'P':
            self.pkd_raport(api, self.pkd_P_result, argument['Regon'], raport_type['P'][1])    
            self.common_raport(api, argument['Regon'], self.common_P_result, raport_type['P'][0])
        elif argument['Typ'] == 'F':
            self.pkd_raport(api, self.pkd_F_result, argument['Regon'], raport_type['F'][1])    
            self.common_raport(api, argument['Regon'], self.common_F_result, raport_type['F'][0])
        elif argument['Typ'] == 'LF':
            self.pkd_raport(api, self.pkd_LF_result, argument['Regon'], raport_type['LF'][1])    
            self.common_raport(api, argument['Regon'], self.common_LF_result, raport_type['LF'][0])
        elif argument['Typ'] == 'LP':
            self.pkd_raport(api, self.pkd_LP_result, argument['Regon'], raport_type['LP'][1])    
            self.common_raport(api, argument['Regon'], self.common_LP_result, raport_type['LP'][0])
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
                    print('Done ', row[1]['Regon'] ,row[1]['Nazwa'])
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





