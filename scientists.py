import re
import pandas as pd
import os.path as op
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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
        'Studia': None, 'Miejsce': None, 'Rok ukończenia': None, 'Profesor_dziedzina': None, 'Profesor_data_nadania_tytułu': None, 'Habilitacja_dziedzina': None, 'Habilitacja_dyscyplina': None,
        'Habilitacja_Data_uzyskania_stopnia': None, 'Habilitacja_Tytuł_pracy': None, 'Habilitacja_Instytucja': None, 'Doktorat_dziedzina': None, 'Doktorat_Dyscyplina': None, 'Doktorat_Specjalność': None,
        'Doktorat_Data_uzyskania_stopnia': None, 'Doktorat_Tytuł_pracy': None, 'Doktorat_Instytucja': None}
        self.employment = []
        self.functions = []
        self.research = []
        self.control_number = 1

    def check_presence(self, xpath: str, desired_text = 'default') -> bool:
        try:
            elem = self.web_driver.find_element_by_xpath(xpath).text
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
        output_dictionary = {prefix + '_ID': None, prefix + '_Type': None, prefix + '_Position': None, prefix +'_Place': None, prefix + '_PlaceID': None}
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
                output_dictionary[prefix + '_PlaceID'] = re.sub(r'[a-zA-Z\:\/\=\?\*\-\.\#]', '', self.web_driver.find_element_by_xpath(f'//*[contains(text(), "{output_dictionary[prefix + "_Place"]}")]').get_attribute('href')) #isolates institution ID from the href
                print(output_dictionary[prefix + '_PlaceID'])
                i += 1 
            else:
                output_dictionary[prefix + '_ID'] = self.main_data['ID']
                output_dictionary[prefix + '_Type'] = current_type
                output_dictionary[prefix + '_Position'] = None
                output_dictionary[prefix +'_Place'] = split_block[i]
                output_dictionary[prefix + '_PlaceID'] = re.sub(r'[a-zA-Z\:\/\=\?\*\-\.\#]', '', self.web_driver.find_element_by_xpath(f'//*[contains(text(), "{output_dictionary[prefix + "_Place"]}")]').get_attribute('href')) #isolates institution ID from the href
                print(output_dictionary[prefix + '_PlaceID'])
                i += 1
            if output_dictionary[prefix +'_Place'] != None and output_dictionary[prefix + '_ID'] != None:
                if prefix == 'emp':
                    self.employment.append(output_dictionary)
                elif prefix == 'func':
                    self.functions.append(output_dictionary)    
                output_dictionary = {prefix + '_ID': None, prefix + '_Type': None, prefix + '_Position': None, prefix +'_Place': None, prefix + '_PlaceID': None}
        print(colors().OKGREEN, self.employment, colors().ENDC)
        print(colors().OKGREEN, self.functions, colors().ENDC)

    def __research_inserter(self, job_name:str, section_number: int) -> None: #inserts research data from given section
        row_number = 1
        while True:
            xpath = (f'//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[{self.control_number}]/div/div/div/section/div/div[{section_number}]/div[2]/div/div/div/div/table/tbody/tr[{row_number}]/td[2]')
            research_dictionary = {'res_ID':None, 'res_Job': None, 'res_Title': None, 'res_reesearchID': None, 'res_Osoby_powiązane_z_pracą': None, 'res_Instytucje_powiązane_z_pracą': None}
            if self.check_presence(xpath):
                block = self.web_driver.find_element_by_xpath(xpath).text
                split_block = block.split('\n')
                research_dictionary['res_ID'] = self.main_data['ID']
                research_dictionary['res_Job'] = job_name
                research_dictionary['res_Title'] = split_block[0]
                research_dictionary['res_reesearchID'] = split_block[1]
                research_dictionary['res_Osoby_powiązane_z_pracą'] = split_block[3]
                research_dictionary['res_Instytucje_powiązane_z_pracą'] = split_block[5]
                # print(colors().WARNING, 'adding dictionary ', research_dictionary, f' with section number {section_number} and row number {row_number}', colors().ENDC)
                self.research.append(research_dictionary)
                row_number += 1
            else:
                break

    def __research_collector(self): #iterates through research sections and triggters __reseatch_inserter method
        jobs = []
        i = 1
        while True:
            if self.check_presence(f'//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[{self.control_number}]/div/div/div/section/div/div[{i}]/div[1]/h4/a/span[1]'):
                jobs.append(self.web_driver.find_element_by_xpath(f'//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[{self.control_number}]/div/div/div/section/div/div[{i}]/div[1]/h4/a/span[1]').text)
                i += 1
            else:
                break
        section_number = 1
        for item in jobs:
            self.__research_inserter(item, section_number)
            section_number += 1
        print(self.research)    

    def data_getter(self):
        self.switcher()
        main_data = []
        main_data.append(self.main_data)
        return main_data, self.employment, self.functions, self.research
        
class document_handler():
    def __init__(self, sex: str, web_driver) -> None:
        self.main_name = f'main_{sex}_scientists.csv'                
        self.research_name = f'research_{sex}_scientists.csv'
        self.employment_name = f'employment_{sex}_scientists.csv'
        self.functions = f'functions_{sex}_scientists.csv'
        self.driver = web_driver

    def __write_single_file(self, name: str, data_frame) -> None:
        if op.exists(name):
            data_frame.to_csv(name, sep=';', header = False, index=False, encoding='UTF-8', mode='a')
        else:
            data_frame.to_csv(name, sep=';', header = True, index=False, encoding='UTF-8', mode='a')


    def main_writer(self) -> None:
        data = data_collector(self.driver).data_getter()
        main_df = pd.DataFrame(data[0])
        emp_df = pd.DataFrame(data[1])
        func_df = pd.DataFrame(data[2])
        res_df = pd.DataFrame(data[3])
        self.__write_single_file(self.main_name, main_df)
        self.__write_single_file(self.employment_name, emp_df)
        self.__write_single_file(self.functions, func_df)
        self.__write_single_file(self.research_name, res_df)

class website_handler():
    def __init__(self, web_driver):
        self.driver = web_driver
        self.names = []

    def __click_button(self, xpath: str) -> None:
        if data_collector(self.driver).check_presence(xpath): #checking presence of button
            self.driver.find_element_by_xpath(xpath).click()
            print(colors().WARNING, 'button clicked', colors().ENDC)

    def __show_more_names(self): #
        options = Select(self.driver.find_element_by_id('inlineSelect'))
        options.select_by_visible_text('100')
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/div/form/button').click()
        input('should be clicked ')

    def __load_current_name(self, current_index: int):
        script = f'''window.open("{self.names[current_index].get_attribute('href')}","_blank");'''
        self.driver.execute_script(script) #exectuing js script that opens new browser tab with spceified scientist's profile 
        self.driver.switch_to.window(self.driver.window_handles[-1]) #switching to new tab
        sleep(0.5)
        self.__click_button('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a') #clicking small button
        try: 
            self.__click_button('//*[@id="content"]/div/div[2]/div[1]/main/section/section/div/div/div/div/button') #clicking bigger button
        except:
            print(colors().FAIL, 'entering exception', colors().ENDC)
            self.driver.find_element_by_class_name('btn-primary nnp-collapsed-button btn btn-lg btn-default').click()
        sleep(0.5)
        document_handler('Male', self.driver).main_writer() #reading data from website and writing them to files 
        self.driver.close() #closing new tab 
        self.driver.switch_to.window(self.driver.window_handles[0]) #switching to main tab 

    def __read_new_names(self, beggining_number: int, num_to_add = 100) -> None:
        for i in range(beggining_number, beggining_number + num_to_add):
            element = self.driver.find_element_by_xpath(f'//*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[{i}]/h2/a')
            self.names.append(element)

    def __start_sequence(self):
        self.names[0].click()
        self.driver.back()

    def tester(self) -> None:
        self.__show_more_names()
        input('enter first name and then go back ')
        self.__read_new_names(1, 100)
        # self.__load_current_name(0)
        # self.__load_current_name(1)
        for i in range(len(self.names)):
            print(i, '. ', self.names[i].text)

    def main_looper(self): #needs check 
        self.__show_more_names()
        input('enter first name and then go back ')
        self.__read_new_names(1, 100)
        print(colors().WARNING, f'len of names is {len(self.names)}', colors().ENDC)
        for i in range(len(self.names)):
            if i % 99 != 0 or i == 0:
                try:
                    self.__load_current_name(i)
                except NoSuchElementException:
                    print(colors().FAIL, 'exception occured, continue? (y/n)', colors().ENDC)
                    response = input()
                    if response == 'y':
                        self.__load_current_name(i)
                    elif response == 'n':
                        break
            else:
                print(colors().WARNING, f'i is {i}', colors().ENDC)
                self.__show_more_names()
                self.__read_new_names(i, i + 100)

    def insert_text(self, value: str) -> None:
        script_text = f'''document.getElementsByClassName("form-control")[1].value="{value}";'''
        try:
            self.driver.execute_script(script_text)
            self.driver.execute_script('''document.getElementsByClassName("btn-primary")[1].click();''')
            input('waiting')
        except Exception as e:
            print('fail', e)
            return
        # ActionChains(self.driver).move_to_element(text_field).send_keys(value).perform()
        

def main():
    dictionaries = []
    driver = webdriver.Chrome()
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=202533&_k=5py0p0')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=225261&_k=2m5mzl')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=25983&_k=488av6')
    # driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a').click()
    # driver.get('https://nauka-polska.pl/#/results?_k=uc5gg9')
    driver.get('https://nauka-polska.pl/#/results?_k=iqbuno') # main page 
    start = input('start ')
    # data_collector(driver).switcher()
    # document_handler('Male', driver).main_writer()
    # website_handler(driver).main_looper()
    website_handler(driver).insert_text('Konrad Pylak')

    driver.close()

if __name__ == '__main__':
    main()


# //*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[1]/h2
# //*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[1]/h2/strong
# //*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[27]/h2
# //*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[96]/h2/a
# //*[@id="content"]/div/div[2]/div[1]/main/section/div/div[2]/div/section/div[2]/div[2]/ul/li[100]/h2/a