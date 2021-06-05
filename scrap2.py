from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

list_of_streets = []


current_town = None
current_municipility = None

class page_hanlder():
    # current_street = None
    web_driver = None
    mode  = str
    counter = 0
    town_counter = 0
    municipility_counter = 0
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

    def __init__(self, driver, mode):
        # self.current_street = current_street
        self.web_driver = driver
        self.mode = mode

    def get_municipilities_list(self):
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]'))
        self.municipilities_options = self.list_of_municipilities.options
        self.current_municipility = self.municipilities_options[self.municipility_counter].get_attribute("value")
    
    def get_street_list(self):
        self.list_of_streets = Select(self.web_driver.find_element_by_xpath('//*[@id="selUlica"]'))
        self.options = self.list_of_streets.options
        self.counter = 0
        self.current_street = self.options[self.counter].get_attribute('value')
    
    def get_towns_lists(self):
            self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
            self.towns_options = self.list_of_towns.options
            self.town_counter = 0
            self.current_town = self.towns_options[self.town_counter].get_attribute('value')

    def empty_page(self):
        try:
            message = self.web_driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text
            if message == 'Nie znaleziono podmiotów':
                return True
            else:
                return False
        except:
            return False

    def change_street(self):
        if self.current_street == self.options[-1].get_attribute('value'):
            self.mode = 't'
            self.change_town()
            
        else:
            print('przystę[uję do zmiany ulicy')
            search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
            wanted_street = self.options[self.counter + 1].get_attribute('value')
            self.list_of_streets.select_by_value(wanted_street)
            search_button.click()
            self.current_street = wanted_street
            self.counter += 1
            self.last_number = 0
    
    def change_municipility(self):
        search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        wanted_municipility = self.municipilities_options[self.municipility_counter + 1].get_attribute('value')    
        self.list_of_municipilities.select_by_value(wanted_municipility)
        self.municipility_counter += 1
        self.current_municipility = wanted_municipility
        self.town_counter = 0
        search_button.click()

    def change_town(self):
        if self.current_town == self.towns_options[-1].get_attribute('value'):
            self.change_municipility()
            self.get_towns_lists()
        else:
            search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
            wanted_town = self.towns_options[self.town_counter + 1].get_attribute('value')
            self.list_of_towns.select_by_value(wanted_town)
            self.current_town = wanted_town
            self.town_counter += 1
            time.sleep(0.4)
            self.get_street_list()
            print('pobrałem listę ulic po zmianie miasta')
            self.counter = 0
            if len(self.options) != 1:
                print('wszedłem w pierwszego if')
                self.mode = 's'
                self.counter = 0
                self.change_street()
            else:
                print('wchpdzę w else')
                search_button.click()
                

            
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



    
    


def write_file():
    pass

def making_item(companies_list, rows):
    i = 1
    for row in rows: 
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
                companies_list.append(item)        
    print('DONE')
    
def count_rows(driver):
    rows = []
    element = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[1]')
    num = 2
    while(True):
                rows.append(element)
                try:
                    element = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]' %num)
                    num += 1
                except:
                    break
    return rows


if __name__ == '__main__':
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    mode = input('Type s for streets t for towns ')
    while mode not in ('s', 't'):
        mode = input('Type s for streets t for towns ')
    pageHandler = page_hanlder(driver, mode)
    i = 0
    pageHandler.get_municipilities_list()
    pageHandler.get_towns_lists()
    while True:
        pageHandler.check_status()
        time.sleep(1)
        # print('next iteration')
        i += 1