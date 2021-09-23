from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, NoAlertPresentException
import time
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get('https://nauka-polska.pl/#/profile/scientist?id=25983&_k=488av6')
s = input('start')
# block = driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[1]/div/div/div/section/div/div[2]/div[2]/div/div/div[1]')
temp = driver.find_elements_by_class_name('nnp-profile-section-title')
for item in temp:
    print(item.text)
driver.close()