from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

list_of_streets = []
current_street = None

class page_hanlder():
    # current_street = None
    web_driver = None
    mode  = str
    counter = 0
    list_of_streets = None
    options = None
    last_number = None

    def __init__(self, current_street, driver, mode):
        # self.current_street = current_street
        self.web_driver = driver
        self.mode = mode

    def get_all_streets(self):
        self.list_of_streets = Select(self.web_driver.find_element_by_xpath('//*[@id="selUlica"]'))
        self.options = self.list_of_streets.options
        current_street = self.options[self.counter].get_attribute('value')

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
        search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        wanted_street = self.options[self.counter + 1].get_attribute('value')
        self.list_of_streets.select_by_value(wanted_street)
        search_button.click()
        self.counter += 1
        self.last_number = 0
    def change_town(self):
        pass

    def change_selector(self):
        if self.mode == 's':
            print('Next Street')
            self.change_street()
        else:
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
    pageHandler = page_hanlder(current_street, driver, mode)
    pageHandler.get_all_streets()
    i = 0
    while i < 6:
        pageHandler.check_status()
        time.sleep(0.5)
        print('next iteration')
        i += 1