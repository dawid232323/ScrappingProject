# import scrap2
from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

class Listener(AbstractEventListener):
    def after_click(self, element, driver):
        print("After click")

def main():
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    edriver = EventFiringWebDriver(driver, Listener())
    edriver.get(url)
    t = input('start')

    page = scrap2.page_hanlder(edriver, 's')
    state = page.get_county_name()
    data = scrap2.data_handler(page, edriver, state)
    system = scrap2.system_handler('toruński', data)
    
    i = 0
    while True:
        page.check_status()
        i += 1
    # page.emergency_refresh()


if __name__ == '__main__':
    main()