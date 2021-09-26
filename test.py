from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
s = input('start')
block = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[5]/div/div/div').text
split_items = block.split('\n')
for i in range(len(split_items)):
    print(i, ' ', split_items[i])
driver.close()