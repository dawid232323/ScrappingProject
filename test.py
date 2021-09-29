from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
original_window = driver.current_window_handle
s = input('start')
button  = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/div/div/div/div/button')
button.click()
input('end ')
driver.close()