import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multipledispatch import dispatch


class data_collector():
    def __init__(self, driver):
        self.web_driver = driver
        self.output = {'ID': None, 'Imie': None, 'Nazwisko': None, 'Specjalności' : None, 'Klasyfikacja': None, 'Powiązane profile': None,
        'Studia': None, 'Miejsce': None, 'Rok ukończenia': None}

    @dispatch(str)
    def __check_presence(self, xpath:str) -> bool:
        try:
            self.web_driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False 

    @dispatch(str, str)
    def __check_presence(self, xpath: str, desired_text: str) -> bool:
        try:
            elem = self.web_driver.find_element_by_xpath(xpath).text.removeprefix(' ')
            print('elem is', elem)
            if  elem == desired_text:
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def switcher(self) -> None: 
        self.__summary_data_collector()
        if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/h2', 'STUDIA'): #checking if education box is present 
            self.__education_collector() #collecting eduaction data 
        if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/h2', 'STOPNIE I TYTUŁY'): #checking if titles and degrees are present 
            print('entering collector')
            self.__titles_collector()
        if self.__check_presence('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/h2'):
            print('dziala') #checking if titles and degrees are present 
        print(self.output)
         

    def __education_collector(self) -> None:
        self.output['Studia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/h4').text
        self.output['Miejsce'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/div/div[1]').text
        self.output['Rok ukończenia'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div/div/div[2]/div[2]/span').text

    def  __summary_data_collector(self) -> None:
        self.output['ID'] = ''.join(re.findall(r'\d+', self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/h1/small[2]/span').text))
        names = [str(i) for i in re.sub(r'prof\.?\ |dr\.?\ |hab\.?\ |inż\.?\ |mgr\.?\ ', '', self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/h1/span').text).split(' ') if i != '']
        if len(names) == 2:
            self.output['Imie'] = names[0]
            self.output['Nazwisko'] = names[1]
        else:
            self.output['Imie'] = ' '.join(names[0:-1])
            self.output['Nazwisko'] = names[-1]
        self.output['Specjalności'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/section/div/div[1]/div[2]/span').text
        self.output['Klasyfikacja'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/section/div/div[2]/div[2]/span').text
        self.output['Powiązane profile'] = self.web_driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/header/div/div[1]/div[2]/section/div/div[3]/div[2]/div/a').text


    def __titles_collector(self) -> None:
       headers = ('Profesor', 'Habilitacja', 'Doktorat')
       block = self.web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div')
       print(block) 
        


def main():
    dictionaries = []
    driver = webdriver.Chrome()
    driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
    # driver.get('https://nauka-polska.pl/#/profile/scientist?id=225261&_k=2m5mzl')
    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a').click()
    start = input('start ')
    data_collector(driver).switcher()
    driver.close()

if __name__ == '__main__':
    main()
