from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

# //*[@id="selUlica"]
# //*[@id="spanPageIndex"]
# //*[@id="selUlica"] xpath do listy ulic 

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

lis = Select(driver.find_element_by_xpath('//*[@id="selUlica"]'))
options = lis.options
print(options, len(options), sep='\n')
# wanted_street = options[1]
# wanted_street_value = wanted_street.get_attribute("value")
# print(wanted_street_value)
# lis.select_by_value(wanted_street_value)
# time.sleep(2)
# driver.close()
