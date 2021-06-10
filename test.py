from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

# //*[@id="selUlica"]
# //*[@id="spanPageIndex"]
# //*[@id="selUlica"] xpath do listy ulic 

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


url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
driver = webdriver.Chrome()
driver.get(url)
test = input("Zaczynamy")
i = 0
# while i < 5:
#     next_page = driver.find_element_by_xpath('//*[@id="btnNextPage"]')
#     next_page.click()
#     time.sleep(1)
#     i += 1

lis = Select(driver.find_element_by_xpath('//*[@id="selMiejscowosc"]'))
options = lis.options
print(options, len(options), sep='\n')
states = Select(driver.find_element_by_xpath('//*[@id="selWojewodztwo"]'))
selected_option = states.first_selected_option
print(selected_option.text)


# name1 = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[1]/td[1]').text
# name10 = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[10]/td[1]').text
# if name1 == name10 == '':
#         print('name 1 is :', name1, '\nname10 is ', name10)

print('robie komunikat', driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text)
if 'Nie znaleziono podmiotów' == driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text:
        print('ruwna sie')
# wanted_street = options[1]
# wanted_street_value = wanted_street.get_attribute("value")
# print(wanted_street_value)
# lis.select_by_value(wanted_street_value)
# time.sleep(2)
# driver.close()
# driver.refresh()