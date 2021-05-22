from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time

# //*[@id="selUlica"]
# //*[@id="spanPageIndex"]
url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(0.5)
print('zaczynam')
print(driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text)
