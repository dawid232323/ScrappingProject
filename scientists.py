import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class data_collector():
    def __init__(self, driver):
        self.web_driver = driver
        self.main_data = {'ID': None, 'Imie': None, 'Nazwisko': None, 'Specjalności' : None, 'Klasyfikacja': None, 'Powiązane profile': None,
        'Studia': None, 'Miejsce': None, 'Rok ukończenia': None}
        self.employment = []
        self.functions = []
        self.research = []
        self.control_number = 1

    def __check_presence(self, xpath: str, desired_text = 'default') -> bool:
        try:
            elem = self.web_driver.find_element_by_xpath(xpath).text#.removeprefix(' ')
            if  elem == desired_text and desired_text != 'default':
                return True
            elif desired_text == 'default':
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def switcher(self) -> dict: 
        self.__summary_data_collector()
        headers = self.web_driver.find_elements_by_class_name('nnp-profile-section-title')
        for item in headers:
            rd_item = item.text
            if rd_item == 'STUDIA':
                self.__education_collector()
                self.control_number += 1
            elif rd_item == 'STOPNIE I TYTUŁY':
                self.__titles_collector()
                self.control_number += 1
            elif rd_item == 'ZATRUDNIENIE':
                self.__employment_functions_collector('emp')
                self.control_number += 1 
            elif rd_item == 'FUNKCJE I CZŁONKOSTWA':
                self.__employment_functions_collector('func')
                self.control_number += 1
            elif rd_item == 'PRACE BADAWCZE':
                self.__research_collector()
                self.control_number += 1

    def __education_collector(self) -> None:
        self.main_data['Studia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section/div/div/h4' % self.control_number).text
        self.main_data['Miejsce'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section/div/div/div/div[1]' % self.control_number).text
        self.main_data['Rok ukończenia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section/div/div/div/div[2]/div[2]/span' % self.control_number).text

    def  __summary_data_collector(self) -> None:
        headers = ('Specjalności', 'Klasyfikacja', 'Powiązane profile')
        self.main_data['ID'] = ''.join(re.findall(r'\d+', self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/h1/small[2]/span').text))
        names = [str(i) for i in re.sub(r'prof\.?\ |dr\.?\ |hab\.?\ |inż\.?\ |mgr\.?\ ', '', self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/h1/span').text).split(' ') if i != '']
        if len(names) == 2:
            self.main_data['Imie'] = names[0]
            self.main_data['Nazwisko'] = names[1]
        else:
            self.main_data['Imie'] = ' '.join(names[0:-1])
            self.main_data['Nazwisko'] = names[-1]
        header_block = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/section/div')
        split_header_block = header_block[0].text.split('\n')
        for item in split_header_block:
            if item.find('@') != -1:
                self.main_data['email'] = item
            elif item in headers:
                self.main_data[item] = split_header_block[split_header_block.index(item) + 1]
            

    def __titles_collector(self) -> None:
       headers = ('Profesor', 'Habilitacja', 'Doktorat')
       block = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section/div' % self.control_number)
       split_items = block[0].text.split('\n')
       for item in split_items:
            if item in headers:
               base_name = item
            elif item == '(Mniej)':
                continue
            else:
                ready_key = item.split(':')
                if len(ready_key) == 2:
                    key_name = base_name + '_' + ready_key[0].replace(' ', '_')
                    self.main_data[key_name] = ready_key[1]
                else:
                    self.main_data[base_name + '_default'] = ready_key[0]

    def __employment_functions_collector(self, prefix:str) -> None: 
        output_dictionary = {prefix + '_ID': None, prefix + '_Type': None, prefix + '_Position': None, prefix +'_Place': None}
        temp = self.web_driver.find_elements_by_class_name('nnp-tab-item-title')
        positions = set()
        for item in temp:
            positions.add(item.text)
        del(temp)
        current_type = str
        types = ('AKTUALNE', 'HISTORYCZNE')
        block = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section' % self.control_number).text 
        #reads whole block with employment rows, then it is converted to simple string and split by new line 
        split_block = block.split('\n')
        i = 0
        while i != len(split_block) - 1: 
            if ''.join(re.findall(r'[A-Z]{11}|[A-Z]{8}', split_block[i])) in types:
                current_type = ''.join(re.findall(r'[A-Z]{11}|[A-Z]{8}', split_block[i]))
                i += 1
            elif split_block[i] in positions:
                output_dictionary[prefix + '_ID'] = self.main_data['ID']
                output_dictionary[prefix + '_Type'] = current_type
                output_dictionary[prefix + '_Position'] = split_block[i]
                output_dictionary[prefix +'_Place'] = split_block[i + 1]
                i += 1 
            else:
                output_dictionary[prefix + '_ID'] = self.main_data['ID']
                output_dictionary[prefix + '_Type'] = current_type
                output_dictionary[prefix + '_Position'] = None
                output_dictionary[prefix +'_Place'] = split_block[i]
                i += 1
            if output_dictionary[prefix +'_Place'] != None and output_dictionary[prefix + '_ID'] != None:
                if prefix == 'emp':
                    self.employment.append(output_dictionary)
                elif prefix == 'func':
                    self.functions.append(output_dictionary)    
                output_dictionary = {prefix + '_ID': None, prefix + '_Type': None, prefix + '_Position': None, prefix +'_Place': None}
        print(colors().OKGREEN, self.employment, colors().ENDC)
        print(colors().OKGREEN, self.functions, colors().ENDC)

    def __research_collector(self):
        jobs = ('Recenzent', 'Promotor', 'Kierownik', 'Wykonawca')
        research_dictionary = {'res_ID':None, 'res_Job': None, 'res_Title': None, 'res_reesearchID': None, 'res_Osoby_powiązane_z_pracą': None, 'res_Instytucje_powiązane_z_pracą': None}
        block = block = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[%d]/div/div/div/section' % self.control_number).text 
        split_block = block.split('\n')
        current_job = str
        i = 0
        while i != len(split_block) - 1:
            if re.sub('[\ ]*Mniej', '', split_block[i]) in jobs:
                current_job = re.sub('[\ ]*Mniej', '', split_block[i])
                i += 1
            else:
                research_dictionary['res_ID'] = self.main_data['ID']
                research_dictionary['res_Job'] = current_job
                research_dictionary['res_Title'] = re.findall(r'[^1-9]\ .*', split_block[i])
                research_dictionary['res_researchID'] = split_block[i + 1]
                research_dictionary['res_Osoby_powiązane_z_pracą'] = split_block[i + 3]
                research_dictionary['res_Instytucje_powiązane_z_pracą'] = split_block[i + 5]
                self.research.append(research_dictionary)
                research_dictionary = {'res_ID':None, 'res_Job': None, 'res_Title': None, 'res_reesearchID': None, 'res_Osoby_powiązane_z_pracą': None, 'res_Instytucje_powiązane_z_pracą': None}
                i += 4

        for item in self.research:
            print(item)

    def data_getter(self):
        return self.main_data, self.employment, self.functions, self.research
        
        


def main():
    dictionaries = []
    driver = webdriver.Chrome()
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=202533&_k=5py0p0')
    driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=225261&_k=2m5mzl')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=25983&_k=488av6')
    # driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a').click()
    start = input('start ')
    data_collector(driver).switcher()
    driver.close()

if __name__ == '__main__':
    main()


# //*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div
# //*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div
# //*[@id="content"]/div/div[2]/div[1]/main/section/section/section[3]/div/div/div