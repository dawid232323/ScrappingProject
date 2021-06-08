from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select
import pandas as pd 
import xlsxwriter
import os 

list_of_streets = []


current_town = None
current_municipility = None

class page_hanlder():
    # current_street = None
    web_driver = None
    mode  = str
    counter = 1
    town_counter = 1
    municipility_counter = 1
    list_of_streets = None
    list_of_towns = None
    list_of_municipilities = None
    options = None
    municipilities_options = None
    towns_options = None
    last_number = None
    current_town = None
    current_street = None
    current_municipility = None
    # current_state = None
    # current_county = None

    def __init__(self, driver, mode):
        # self.current_street = current_street
        self.web_driver = driver
        self.states_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selWojewodztwo"]'))
        self.current_state = self.states_list.first_selected_option.get_attribute('value')
        self.counties_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selPowiat"]'))
        self.current_county = self.counties_list.first_selected_option.get_attribute('value')
        self.mode = mode
        if self.mode == 't':
            self.town_counter = 1
        elif self.mode == 's':
            self.counter = 1

    def get_municipilities_list(self): #function that changes municipility and gets all states and counties during initialozation. States and counties are used during the refresh
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]'))
        self.municipilities_options = self.list_of_municipilities.options
        self.current_municipility = self.municipilities_options[self.municipility_counter].get_attribute("value") #current municipility is the one on the counter's position. Counter is never changed after init at tths moment
    
    def get_street_list(self): #function that gets all the streets. It is called whenever the town is changed
        self.list_of_streets = Select(self.web_driver.find_element_by_xpath('//*[@id="selUlica"]'))
        self.options = self.list_of_streets.options
        self.counter = 1 #counter is set to one, because 'rozwiń' is on the 0 position
        while len(self.options) == 0: #mechanism that waits for the streets list to load
            print("czekam na listę ulic")
            time.sleep(0.3)
            self.options = self.list_of_streets.options
        if len(self.options) > 1: #current street is dependent to list size. If size is greater than one it means that there are streets in the town
            self.current_street = self.options[self.counter].get_attribute('value')
        else:
            self.current_street = self.options[0].get_attribute('value')
    
    def get_towns_lists(self): #function that gets all the towns in a municipility. It is called after every municipility change
            self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
            self.towns_options = self.list_of_towns.options
            # self.town_counter = 1 #counter is set to one, because position 0 is 'rozwiń'
            while len(self.towns_options) == 0: #mechanism that waits for towns list to load
                print('czekam na listę miast')
                time.sleep(0.3)
                self.towns_options = self.list_of_towns.options
            self.current_town = self.towns_options[self.town_counter].get_attribute('value') #current town is set to first town in the list

    def empty_page(self): #function that checks if page is empty 
        try:
            message = self.web_driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text
            if message == 'Nie znaleziono podmiotów':
                return True
            else:
                return False
        except:
            return False

    def change_street(self): #function that changes street
        if self.current_street == self.options[-1].get_attribute('value'): #if current street is the last one on the list of streets, mode is changed to towns, because at this point we don't konow
            #if next town has streets. Then function to change town is called
            print('ostatnia ulica')
            self.mode = 't'
            self.change_town()
            
        else: #if street is not the last one next one is choosen
            print('przystę[uję do zmiany ulicy')
            search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
            wanted_street = self.options[self.counter + 1].get_attribute('value') #this is the street that option will be changed to. It is on the next postion relative to the counter 
            self.list_of_streets.select_by_value(wanted_street)
            search_button.click()
            self.current_street = wanted_street #current street is changed to the wanted one (that's next street realtive to the current_one)
            self.counter += 1 #position of the counter is changed
            self.last_number = 0 #last number represents amount of pages displayed so far 
    
    def change_municipility(self): #function that changes municipility to the next one 
        # search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        wanted_municipility = self.municipilities_options[self.municipility_counter + 1].get_attribute('value') #wanted municipility is the next one relative to the current one    
        self.list_of_municipilities.select_by_value(wanted_municipility)
        self.municipility_counter += 1 #counter of municipilities is increased by one
        self.current_municipility = wanted_municipility #current municipility is changed to the next one 
        self.town_counter = 0 #town counter is 0, because in the change town function, wanted town is counter + 1, so if it was equal to 1, we would skip the first item 
        self.counter = 1
        time.sleep(1)
        self.get_towns_lists() #becuase municipility is changed, we need new list of towns
        print('pobrałem liste miast po zmianie gminy')
        print('długość listy miast ', len(self.towns_options), 'ostatni element:', self.towns_options[-1].text)
        self.change_town() #because town field is empty, we need to change it to the first one. Because of town counter equal to 0, wanted town in this function becomes the first one on the list 
        # search_button.click()

    def search_for_popup(self):
        try:
            self.web_driver.switchTo().alert().accept()
            return False
        except Exception:
            return True

    def change_town(self):
        if self.current_town == self.towns_options[-1].get_attribute('value') and len(self.towns_options) != 2:
            print('ostatnie miasto', self.towns_options[-1].text)
            self.change_municipility()
        elif self.current_town == self.towns_options[-1].get_attribute('value') and len(self.towns_options) == 2:
            print('wchodzę w elif')
            street_copy = self.options[1].text 
            self.get_street_list()
            if street_copy == self.options[1].text:
                print('zmieniam gminę, po przejściu całego miasta')
                self.change_municipility()
            else:
                self.mode = 's'
                self.counter = 1
            
            self.change_street()
        else:
            search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
            wanted_town = self.towns_options[self.town_counter + 1].get_attribute('value')
            self.list_of_towns.select_by_value(wanted_town)
            self.current_town = wanted_town
            self.town_counter += 1
            time.sleep(0.4)
            self.get_street_list()
            print('pobrałem listę ulic po zmianie miasta')
            self.counter = 1
            search_button.click()
            if not self.search_for_popup():
                print('wszedłem w pierwszego if')
                self.mode = 's'
                self.counter = 1
                self.change_street()
            
    def change_selector(self):
        if self.mode == 's':
            print('Next Street')
            self.change_street()
        elif self.mode == 't':
            print('Next Town')
            self.change_town()

    def next_page(self):
        next_page = self.web_driver.find_element_by_xpath('//*[@id="btnNextPage"]')
        next_page.click()
        time.sleep(0.5)

    def check_status(self):
        
        print('Checking status')
        if self.empty_page():
            self.change_selector()
        else:
            element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
            result = element.split('/')
            if len(result) == 1:
                self.change_selector()
            else:
                if (int(result[0]) < int(result[1])):
                    print(result[0])
                    print('changing page')
                    self.last_number = result[0]
                    self.next_page()
                    element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
                    result = element.split('/')
                    while result[0] == self.last_number:
                        time.sleep(0.25)
                        # self.next_page()
                        element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
                        result = element.split('/')

                else:
                    self.change_selector()

    def emergency_refresh(self):
        las_number_copy = self.last_number
        current_municipility_copy = self.current_municipility
        current_town_copy = self.current_town
        current_street_copy = self.current_street
        current_state_copy = self.current_state
        current_county_copy = self.current_county
        counters_copy = [self.counter, self.town_counter, self.municipility_counter]
        self.web_driver.refresh()
        time.sleep(3)
        addres_button = self.web_driver.find_element_by_xpath('//*[@id="btnMenuSzukajPoAdresie"]')
        addres_button.click()
        time.sleep(3)
        self.list_of_states = Select(self.web_driver.find_element_by_xpath('//*[@id="selWojewodztwo"]')) 
        self.list_of_states.select_by_value(current_state_copy)
        time.sleep(0.5)
        self.counties_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selPowiat"]'))
        self.counties_list.select_by_value(current_county_copy)
        time.sleep(0.5)
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]')) 
        self.list_of_municipilities.select_by_value(current_municipility_copy)
        time.sleep(0.5)
        self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
        self.list_of_towns.select_by_value(current_town_copy)
        time.sleep(0.5)
        search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        self.get_municipilities_list()
        self.get_towns_lists()
        self.get_street_list()
        self.counter = counters_copy[0]
        self.town_counter = counters_copy[1]
        self.municipility_counter = counters_copy[2]
        if len(self.options) != 1:
            self.list_of_streets.select_by_value(current_street_copy)
        search_button.click()
        time.sleep(0.5)
        if int(self.last_number) > -1:
            current_number = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
            result = current_number.split('/')
            while result[0] != self.last_number:
                self.next_page()
                current_number = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
                result = current_number.split('/')

    def get_county_name(self):
        return self.counties_list.first_selected_option.text
    
    

class data_handler():

    def __init__(self, page_handler, driver, state):
        self.page_handler = page_handler
        self.rows = []
        self.companies_list = []
        self.web_driver = driver
        self.current_output_number = 1
        self.current_state_name = state

    def count_rows(self):
        element = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[1]')
        num = 2
        while(True):
                    self.rows.append(element)
                    try:
                        element = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]' %num)
                        num += 1
                    except:
                        print('policzyłem rekordy')
                        break
        

    def making_item(self):
        print('zaczyanm czytać tabele')
        i = 1
        for row in self.rows: 
                    regon = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[1]' % i).text
                    type = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[2]' %i).text
                    name = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[3]' % i).text
                    state = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[4]' % i).text
                    county = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[5]' % i).text
                    community = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[6]' % i).text
                    postalCode = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[7]' % i).text
                    city = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[8]' % i).text
                    street = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[9]' % i).text
                    deleted = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[10]' % i).text
                    i += 1
                    item = {'Regon': regon, 'Typ': type, 'Nazwa': name, 'Województwo': state, 'Powiat': county, 'Gmina': community, 
                    "Kod Pocztowy": postalCode, 'Miasto': city, 'Ulica': street, 'Informacja u usniętym wpisie': deleted}
                    self.companies_list.append(item)        
        self.rows.clear()
        print('DONE')
        
    def write_file(self):
        data_frame = pd.DataFrame(self.companies_list)
        name = str(self.current_state_name) + '_' + str(self.current_output_number) + '.xlsx'
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        data_frame.to_excel(writer, sheet_name='sheet1', header=False, index=False)
        writer.save()
        self.current_output_number += 1
        self.companies_list.clear()

def make_new_directory(current_state_name):
    path = os.getcwd()
    wanted_path = path + '/' + current_state_name
    try:
        os.mkdir(wanted_path)
        os.chdir(wanted_path)
    except Exception as ex:
        print(ex)


    


if __name__ == '__main__':
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    mode = input('Type s for streets t for towns ')
    while mode not in ('s', 't'):
        mode = input('Type s for streets t for towns ')
    pageHandler = page_hanlder(driver, mode)
    county_name = pageHandler.get_county_name()
    dataHandler = data_handler(pageHandler, driver, county_name)
    i = 0
    pageHandler.get_municipilities_list()
    pageHandler.get_towns_lists()
    pageHandler.get_street_list()
    make_new_directory(county_name)
    i = 0
    while i < 20:
        try:
            dataHandler.count_rows()
            dataHandler.making_item()
        except:
            time.sleep(0.5)
            continue
        if i%10 == 0:
            dataHandler.write_file()
        pageHandler.check_status()
        time.sleep(1)
        # print('next iteration')
        i += 1

    dataHandler.write_file()