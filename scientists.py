import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multipledispatch import dispatch

class data_collector():
    def __init__(self, driver):
        self.web_driver = driver
        self.main_data = {'ID': None, 'Imie': None, 'Nazwisko': None, 'Specjalności' : None, 'Klasyfikacja': None, 'Powiązane profile': None,
        'Studia': None, 'Miejsce': None, 'Rok ukończenia': None}
        self.employment = {'ID': None, 'Type': None, 'Position': None, 'Place': None}

    def __check_presence(self, xpath: str, desired_text = 'default') -> bool:
        try:
            elem = self.web_driver.find_element_by_xpath(xpath).text.removeprefix(' ')
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
        if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/h2', 'STUDIA'): #checking if education box is present 
            self.__education_collector() #collecting eduaction data 
        if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/h2', 'STOPNIE I TYTUŁY'): #checking if titles and degrees are present 
            print('entering collector')
            self.__titles_collector()
        # if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/h2', 'ZATRUDNIENIE'): #checking if employment box is present
        #     self.__employment_collector()
        self.__test_function()
        print(self.main_data)
        return self.main_data
         

    def __education_collector(self) -> None:
        self.main_data['Studia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/h4').text
        self.main_data['Miejsce'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/div/div[1]').text
        self.main_data['Rok ukończenia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/div/div[2]/div[2]/span').text

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
       block = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div')
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

    def __employment_collector(self) -> None:
        print('in the emp collector')
        types = ('AKTUALNE', 'HISTORYCZNE')
        block = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div')
        print(block[0].text)

    def __test_function(self):
        print('testtinfg')
        elem = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]')
        print(elem[0].text)
        
        


def main():
    dictionaries = []
    driver = webdriver.Chrome()
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=202533&_k=5py0p0')
    driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=225261&_k=2m5mzl')
    # driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a').click()
    start = input('start ')
    data_collector(driver).switcher()
    driver.close()

if __name__ == '__main__':
    main()
