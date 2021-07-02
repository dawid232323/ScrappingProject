import scrap2
from selenium import webdriver
import time

def main():
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    t = input('start')
    page = scrap2.page_hanlder(driver, 't')
    state = page.get_county_name()
    data = scrap2.data_handler(page, driver, state)
    i = 0
    while i < 100:
        page.check_status()
        i += 1
    page.emergency_refresh()
    time.sleep(10)
    i = 0
    while i < 50:
        page.check_status()
        i += 1
        


if __name__ == '__main__':
    main()