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
value = 'https://google.pl'
string = f'''window.open("{value}","_blank");'''
driver.execute_script(string)
window_name = driver.window_handles[-1]
driver.switch_to.window(driver.window_handles[-1])
driver.get('https://www.onet.pl/')
driver.close()
input('middle ')
driver.switch_to.window(driver.window_handles[0])
driver.refresh()
input('end ')
driver.close()