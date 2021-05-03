from litex.regon import REGONAPI
from lxml import etree
from lxml import objectify
import pandas as pd 
import xlsxwriter
import csv

raport_type = {'P':['BIR11OsPrawna', 'BIR11OsPrawnaPkd'] ,
'F':['BIR11OsFizycznaDaneOgolne', 'BIR11OsFizycznaPkd'] ,
'LF':['BIR11JednLokalnaOsFizycznej','BIR11JednLokalnaOsFizycznejPkd'],
 'LP':['BIR11JednLokalnaOsPrawnej','BIR11JednLokalnaOsPrawnejPkd']}

class file_handler():
    def __init__(self, input_name):
        self.input_name = input_name

    def open_file(self):
        file = pd.read_csv('regony.csv', sep=';')
        return file

    
    

class Result_Arrays:

    common_P_result = []
    pkd_P_result = []
    common_F_result = []
    pkd_F_result = []
    common_LF_result = []
    pkd_LF_result = []
    common_LP_result = []
    pkd_LP_result = []
    

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def common_raport(self, api, regon, result, cmp_type):
        try:
            root = api.full_report(regon, cmp_type)
        except:
            print(Exception)
        position = {}
        for elem in root.getchildren():
            position[elem.tag] = elem.text
        result.append(position)
        del(position)

    def pkd_raport(self, api, result, regon, cmp_type):
        try:
            root = api.full_report(regon, cmp_type)
        except:
            print(Exception)
        for branch in root:
            position = {}
            for element in branch.getchildren():
                position['regon'] = regon
                position[element.tag] = element.text
            result.append(position)
            del(position)

    def make_spreedsheet(self, result, name):
        df = pd.DataFrame(result)
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1')
        writer.save()

    def emergency_break(self, num):
        self.make_spreedsheet(self.common_P_result, 'common_P%d.xlsx' %num)
        self.make_spreedsheet(self.common_F_result, 'commonF%d.xlsx' %num)
        self.make_spreedsheet(self.common_LF_result, 'commonLF%d.xlsx' %num)
        self.make_spreedsheet(self.common_LP_result, 'commonLP%d.xlsx' %num)
        self.make_spreedsheet(self.pkd_P_result, 'pkd_P%d.xlsx'%num)
        self.make_spreedsheet(self.pkd_F_result, 'pkd_F%d.xlsx'%num)
        self.make_spreedsheet(self.pkd_LF_result, 'pkd_LF%d.xlsx'%num)
        self.make_spreedsheet(self.pkd_LP_result, 'pkd_LP%d.xlsx'%num)
        self.common_F_result.clear()
        self.common_LF_result.clear()
        self.common_LP_result.clear()
        self.common_P_result.clear()
        self.pkd_F_result.clear()
        self.pkd_LF_result.clear()
        self.pkd_LP_result.clear()
        self.pkd_P_result.clear()

    def raport_type(self, argument, api):
        if argument[2] == 'P':
            self.pkd_raport(api, self.pkd_P_result, argument[1], raport_type['P'][1])    
            self.common_raport(api, argument[1], self.common_P_result, raport_type['P'][0])
        elif argument[2] == 'F':
            self.pkd_raport(api, self.pkd_F_result, argument[1], raport_type['F'][1])    
            self.common_raport(api, argument[1], self.common_F_result, raport_type['F'][0])
        elif argument[2] == 'LF':
            self.pkd_raport(api, self.pkd_LF_result, argument[1], raport_type['LF'][1])    
            self.common_raport(api, argument[1], self.common_LF_result, raport_type['LF'][0])
        elif argument[2] == 'LP':
            self.pkd_raport(api, self.pkd_LP_result, argument[1], raport_type['LP'][1])    
            self.common_raport(api, argument[1], self.common_LP_result, raport_type['LP'][0])
        else:
            print('type not found')

    def get_raport(self):
        counter = 0
        num = 1
        api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
        api.login('c5edf702474f47e78ad5')
        for i in range(len(self.data_frame)):
            if counter < 2500:
                try:
                    self.raport_type(self.data_frame.iloc[i], api)
                    # self.data_frame.drop(i, axis=0, inplace=True)
                    # self.data_frame.to_csv('regony.csv', index=False, sep=';')
                    counter += 1  
                    print('Done ', self.data_frame.iloc[i][0] ,self.data_frame.iloc[i][3])
                except Exception as e:
                    print('first if ', e)
                    counter += 1  
                    continue
                
            else:
                try:
                    self.emergency_break(num)
                except:
                    print('emergency ', Exception)
                num +=1
                counter = 0
                try:
                    api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc')
                    api.login('c5edf702474f47e78ad5')
                except:
                    print('api ', Exception)
        self.emergency_break(num)

if __name__ == '__main__':
    files = file_handler('regony.csv')
    arrays = Result_Arrays(files.open_file())
    arrays.get_raport()





