from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
import time


# //*[@id="spanPageIndex"]

raport_type = {'P':['BIR11OsPrawna', 'BIR11OsPrawnaPkd'] ,'F':'BIR11OsFizycznaDaneOgolne' ,'LF':'BIR11JednLokalnaOsFizycznej',
 'LP':'BIR11JednLokalnaOsPrawnej'}

print(raport_type['P'][0])
