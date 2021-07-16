from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
# from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
import time
from selenium.webdriver.support.ui import Select
import pandas as pd 
import xlsxwriter
import os 
import sys
import traceback 
# from scrap_sandbox import Listener

working_switch = True


def exit_programme(dataHandler, driver):
    dataHandler.write_file()
    driver.close()
    print('bye bye')

class colors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'

class page_hanlder():
    mode = str
    counter = 1
    town_counter = 1
    municipility_counter = 1

    def __init__(self, driver, mode):
        # self.current_street = current_street    
        self.web_driver = driver
        self.progress_block = self.web_driver.find_element_by_xpath('//*[@id="divProgressIcon"]')
        self.states_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selWojewodztwo"]'))
        self.current_state = self.states_list.first_selected_option.get_attribute('value')
        self.counties_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selPowiat"]'))
        self.current_county = self.counties_list.first_selected_option.get_attribute('value')
        self.mode = mode
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]'))
        self.municipilities_options = self.list_of_municipilities.options
        self.current_municipility = self.list_of_municipilities.first_selected_option
        self.municipility_counter = self.municipilities_options.index(self.current_municipility)
        self.current_municipility = self.municipilities_options[self.municipility_counter].get_attribute('value')
        self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
        self.towns_options = self.list_of_towns.options
        self.current_town = self.list_of_towns.first_selected_option
        self.town_counter = self.towns_options.index(self.current_town)
        self.current_town = self.towns_options[self.town_counter].get_attribute('value')
        self.list_of_streets = Select(self.web_driver.find_element_by_xpath('//*[@id="selUlica"]'))
        self.options = self.list_of_streets.options
        if self.mode == 's':
            self.current_street = self.list_of_streets.first_selected_option
            self.counter = self.options.index(self.current_street)
            self.current_street = self.options[self.counter]
        else:
            self.counter = 1
        self.goal_number = 0
        self.last_number = -1
        self.working_switch = True

    def wait_for_progress(self):  # method that checks if progress bar is displayed
        try:
            if self.progress_block.is_displayed():
                return True
            else:
                return False
        except:
            self.progress_block = self.web_driver.find_element_by_xpath('//*[@id="divProgressIcon"]')
            if self.progress_block.is_displayed():
                return True
            else:
                return False

    def get_municipilities_list(self):  # function that changes municipility and gets all states and counties during initialozation. States and counties are used during the refresh
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]'))
        self.municipilities_options = self.list_of_municipilities.options
        self.current_municipility = self.municipilities_options[self.municipility_counter].get_attribute("value") #current municipility is the one on the counter's position. Counter is never changed after init at tths moment
    
    def get_street_list(self):  # function that gets all the streets. It is called whenever the town is changed
        self.list_of_streets = Select(self.web_driver.find_element_by_xpath('//*[@id="selUlica"]'))
        self.options = self.list_of_streets.options
        self.counter = 1  # counter is set to one, because 'rozwiń' is on the 0 position
        iterator = 0
        while len(self.options) == 0:  # mechanism that waits for the streets list to load
            if iterator == 20:
                print(f"{colors.FAIL} iterator equals ", iterator, f"{colors.ENDC}")
                self.emergency_refresh()
                break
            print("czekam na listę ulic")
            time.sleep(0.3)
            self.options = self.list_of_streets.options
            iterator += 1
        if len(self.options) > 1:  # current street is dependent to list size. If size is greater than one it means that there are streets in the town
            self.current_street = self.options[self.counter].get_attribute('value')
        else:
            self.current_street = self.options[0].get_attribute('value')
    
    def clone_parameters(self):
        list_of_towns_copy = self.list_of_towns
        towns_options_copy = list_of_towns_copy.options
        current_town_copy = self.current_town
        current_street_copy = self.current_street
        list_of_streets_copy = self.list_of_streets
        street_options_copy = list_of_streets_copy.options
        street_counter_copy = self.counter
        towns_counter_copy = self.town_counter
        copies = [list_of_towns_copy, towns_options_copy, current_town_copy, current_street_copy, street_options_copy, street_counter_copy, towns_counter_copy]
        return copies

    def get_towns_lists(self): #function that gets all the towns in a municipility. It is called after every municipility change
            # copies = self.clone_parameters()
            self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
            self.towns_options = self.list_of_towns.options
            # self.town_counter = 1 #counter is set to one, because position 0 is 'rozwiń'
            wait_iter = 0
            while len(self.towns_options) == 0: #mechanism that waits for towns list to load
                if wait_iter == 20:
                    # self.current_town, self.current_street, self.counter, self.town_counter = copies[2], copies[3], copies[5], copies[-1]
                    self.emergency_refresh()
                    break
                print('czekam na listę miast')
                time.sleep(0.3)
                self.towns_options = self.list_of_towns.options
                wait_iter += 1
            else:
                # del(copies)
                self.current_town = self.towns_options[self.town_counter].get_attribute('value') #current town is set to first town in the list

    def empty_page(self): #function that checks if page is empty and has no data in it 
        try:
            message = self.web_driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text
            if message == 'Nie znaleziono podmiotów.':
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
            self.last_number = -1
            
        else: #if street is not the last one next one is choosen
            print('przystę[uję do zmiany ulicy')
            search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
            wanted_street = self.options[self.counter + 1].get_attribute('value') #this is the street that option will be changed to. It is on the next postion relative to the counter 
            self.list_of_streets.select_by_value(wanted_street)
            search_button.click()
            self.current_street = wanted_street #current street is changed to the wanted one (that's next street realtive to the current_one)
            self.counter += 1 #position of the counter is changed
            self.last_number = -1 #last number represents amount of pages displayed so far 
    
    def change_municipility(self): #function that changes municipility to the next one 
        # search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        if self.current_municipility == self.municipilities_options[-1].get_attribute('value'):
            self.working_switch = False
        else:     
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
        if self.current_town == self.towns_options[-1].get_attribute('value') and len (self.towns_options) != 2: #condition that checks if current city is the last one on the list and if the list contains more than just one position
            print('last town', self.towns_options[-1].text)
            self.change_municipility()
        elif self.current_town == self.towns_options[-1].get_attribute('value') and len(self.towns_options) == 2: #condition that checks if current city is the only one in the municipility 
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
                print('town has to be read by street')
                self.mode = 's'
                self.counter = 1
                self.change_street()
            
    def change_selector(self): #function that checks what should be changed town or street
        if self.mode == 's':
            print('Next Street')
            self.change_street()
        elif self.mode == 't':
            print('Next Town')
            self.change_town()

    def next_page(self): #if there are more that one page in certain town/city this function changes page to the next one 
        next_page = self.web_driver.find_element_by_xpath('//*[@id="btnNextPage"]')
        next_page.click()
        time.sleep(0.5)

    def check_status(self): #function that checks the status of the page 
        
        print('Checking status')
        if self.empty_page(): #if page has no records change selector is called
            self.goal_number = 0
            self.change_selector()
            time.sleep(1) 
        else:
            element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text #line that checks 
            #number of pages displayed so far and number of all the pages on the current street/town 
            result = element.split('/')
            if len(result) == 1: #if lenght of array with numbers equals 1 it means, that there is only one page
                self.last_number = -1
                self.goal_number = 0
                self.change_selector()
            else:
                self.goal_number = int(result[1])
                if (int(result[0]) < int(result[1])): #while the first number is smaller than the second one
                    print(result[0]) #printing current page so it is known 
                    print('changing page')
                    self.last_number = result[0] #last number is needed in case of emergency refresh
                    self.next_page()
                    element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text #same mechanism as higher
                    result = element.split('/')
                    while result[0] == self.last_number: #while we wait for the pages to change, this mechanism stops the program
                        #in skipping pages 
                        time.sleep(0.25)
                        # self.next_page()
                        element = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
                        result = element.split('/')

                else: #if first number equals the second one street/town is changed 
                    self.last_number = -1
                    self.goal_number = 0
                    self.change_selector()

    def emergency_refresh(self): #function that refreshes page after failure and sets it to the last remembered state 
        # las_number_copy = self.last_number
        self.progress_block = self.web_driver.find_element_by_xpath('//*[@id="divProgressIcon"]')        
        current_municipility_copy = self.current_municipility
        current_town_copy = self.current_town
        if self.mode == 's':
            current_street_copy = self.current_street
        current_state_copy = self.current_state
        current_county_copy = self.current_county
        counters_copy = [self.counter, self.town_counter, self.municipility_counter] #copying all parameters
        self.web_driver.refresh() #refreshing page
        time.sleep(3)
        addres_button = self.web_driver.find_element_by_xpath('//*[@id="btnMenuSzukajPoAdresie"]') 
        addres_button.click() #clicking address button
        time.sleep(3)
        self.list_of_states = Select(self.web_driver.find_element_by_xpath('//*[@id="selWojewodztwo"]')) 
        self.list_of_states.select_by_value(current_state_copy) #selecting last state 
        time.sleep(0.5)
        self.counties_list = Select(self.web_driver.find_element_by_xpath('//*[@id="selPowiat"]'))
        self.counties_list.select_by_value(current_county_copy) #selecting last county 
        time.sleep(0.5)
        self.list_of_municipilities = Select(self.web_driver.find_element_by_xpath('//*[@id="selGmina"]')) 
        self.list_of_municipilities.select_by_value(current_municipility_copy) #selecting last municipility
        time.sleep(0.5)
        self.list_of_towns = Select(self.web_driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
        self.list_of_towns.select_by_value(current_town_copy) #selecting last town 
        time.sleep(0.5)
        search_button = self.web_driver.find_element_by_xpath('//*[@id="btnSzukajPoAdresie"]')
        self.get_municipilities_list() 
        self.get_towns_lists()
        self.get_street_list()
        print('pobrałem wszystkie listy')
        self.counter = counters_copy[0]
        self.town_counter = counters_copy[1]
        self.municipility_counter = counters_copy[2] #getting new lists and setting counters 
        print('jestem przed kliknięciem przycisku')
        if self.mode == 't':
            search_button.click()
            print('kliknąłem przycisk')
            self.search_for_popup()
            time.sleep(2)
        else: 
            self.list_of_streets.select_by_value(current_street_copy)
            search_button.click()
            time.sleep(1)
            search_button.click()
        time.sleep(0.5)
        print('będę zmieniał strony')
        if int(self.last_number) > -1: 
            current_number = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
            result = current_number.split('/')
            print('result[0] is ', result[0], 'last number wil be ', self.last_number)
            while int(result[0]) < int(self.last_number):
                try:
                    if self.wait_for_progress():
                        continue
                except Exception:
                    self.progress_block = self.web_driver.find_element_by_xpath('//*[@id="divProgressIcon"]')
                    traceback.print_exc()
                    continue
                try:
                    print('current number ', result[0])
                    self.next_page()
                    # time.sleep(1)
                    current_number = self.web_driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
                    result = current_number.split('/')
                except Exception:
                    continue
                
            

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
        self.regons_check = set()
        self.refresh_control = 0
    

    def making_item(self):
        print('zaczyanm czytać tabele')
        i = 1
        self.regons_check.clear()
        while True:
            try:
                    regon = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[1]' % i).text
                    type = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[2]' %i).text
                    name = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[3]' % i).text
                    state = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[4]' % i).text
                    county = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[5]' % i).text
                    community = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[6]' % i).text
                    postalCode = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[7]' % i).text
                    city = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[8]' % i).text
                    street = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[9]' % i).text
                    deleted = self.web_driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[10]' % i).text
                    i += 1
                    item = {'Regon': regon, 'Typ': type, 'Nazwa': name, 'Województwo': state, 'Powiat': county, 'Gmina': community, 
                    "Kod Pocztowy": postalCode, 'Miasto': city, 'Ulica': street, 'Informacja u usniętym wpisie': deleted}
                    if self.page_handler.empty_page() == False and regon == '' and self.page_handler.goal_number == int(self.page_handler.last_number) + 1: #tutaj dorobić jakiś checker, który przy pierwszej takiej sytuacji jest zwięszany o 1 i wywoływany jest check status, a jeśli pod rząd wydarzy się taka sytuacja, to dopiero wtedy emergency refresh
                        #dodatkowo po refreshu ostatni ostatni numer jest ilością stron, to wtedy nalezy sprawdzić status i w tej funkcji dać continue, tak zeby nie sprawdzac statusu dwa razy
                        print('first strike last_number = ', self.page_handler.last_number, 'goal number = ', self.page_handler.goal_number)
                        self.refresh_control = 1
                        self.page_handler.check_status()
                        time.sleep(2)
                        i = 1
                        continue
                        # break
                    elif self.page_handler.empty_page() == False and regon == '' and self.page_handler.goal_number != int(self.page_handler.last_number) + 1:
                        print('emergency refresh after not equal numbers', self.page_handler.last_number, 'goal number = ', self.page_handler.goal_number)
                        self.write_file()
                        self.page_handler.emergency_refresh()
                        self.refresh_control = 0
                        i = 1
                        continue
                    elif self.page_handler.empty_page() == False and regon == '' and self.refresh_control == 1:
                        print('emergency refresh after refresh control', self.page_handler.last_number, 'goal number = ', self.page_handler.goal_number)
                        self.write_file()
                        self.page_handler.emergency_refresh()
                        i = 1
                        self.refresh_control = 0
                        continue
                    elif regon != '':
                        self.regons_check.add(regon)
                        self.companies_list.append(item) 
                        self.refresh_control = 0
            except Exception:
                # type, value, traceback = sys.exc_info()
                # print('wyjątek przy making item', type, value, traceback)
                break       
        print('DONE')


    def write_file(self):
        data_frame = pd.DataFrame(self.companies_list)
        name = str(self.current_state_name) + '_' + str(self.current_output_number) + '.xlsx'
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        data_frame.to_excel(writer, sheet_name='sheet1', header=False, index=False)
        writer.save()
        self.current_output_number += 1
        self.companies_list.clear()

    def change_output_number(self, output):
        self.current_output_number = output

class system_handler():
    def __init__(self, county, data_handler):
        self.current_county_name = county
        self.current_path = os.getcwd()
        self.data_handler = data_handler
        self.output = 0

    def resume_directory(self):
        import re
        names = os.listdir()
        numbers = []
        for name in names:
            numbers.append(int(re.findall(r'\d+', name)[0]))
        self.output = max(numbers) + 1
        self.data_handler.change_output_number(self.output)
        print('current outupt number = ', self.data_handler.current_output_number)

    def make_new_directory(self):
        path = os.getcwd()
        wanted_path = path + '/' + self.current_county_name
        self.current_path = wanted_path
        try:
            os.mkdir(wanted_path)
            os.chdir(wanted_path)
        except FileExistsError:
            os.chdir(wanted_path)
            print('Directory already exists')
            self.current_path = os.getcwd()
            self.resume_directory()
        except Exception as ex:
            print(ex)


    


if __name__ == '__main__':
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(executable_path='C:\\Users\\dawpy\\Documents\\Scrapping\\chromedriver.exe')
    driver.get(url)
    mode = input('Type s for streets t for towns ')
    while mode not in ('s', 't'):
        mode = input('Type s for streets t for towns ')
    pageHandler = page_hanlder(driver, mode)
    county_name = pageHandler.get_county_name()
    dataHandler = data_handler(pageHandler, driver, county_name)
    system_handler = system_handler(county_name, dataHandler)
    system_handler.make_new_directory()
    iteration_counter = 0
    i = 0
    while pageHandler.working_switch:
        if pageHandler.wait_for_progress():
            continue
        pageHandler.search_for_popup()
        try:
            if pageHandler.empty_page():
                time.sleep(1)
                pageHandler.check_status()
            elif driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[1]/td[1]').text in dataHandler.regons_check:
                if iteration_counter == 5:
                    print('iteration counter equals 50')
                    pageHandler.check_status()
                    iteration_counter = 0
                else:
                    iteration_counter += 1
                    print('regon conflict, iterator is ', iteration_counter)
                    time.sleep(0.5)
                    continue
            else:
                dataHandler.making_item()
                pageHandler.check_status()
                while pageHandler.wait_for_progress():
                    time.sleep(0.2)
                    continue
                iteration_counter = 0
        except KeyboardInterrupt:
            exit_programme(dataHandler, driver)
        except Exception as ex:
            traceback.print_exc()
            exit_programme(dataHandler, driver)
            continue
    exit_programme(dataHandler, driver )