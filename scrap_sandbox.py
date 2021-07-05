import scrap2
from selenium import webdriver
import time

def main():
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    page = scrap2.page_hanlder(driver, 't')
    state = page.get_county_name()
    data = scrap2.data_handler(page, driver, state)
    system = scrap2.system_handler('toruński', data)
    t = input('start')
    system.make_new_directory()


if __name__ == '__main__':
    main()