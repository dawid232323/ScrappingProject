import scrap2
from selenium import webdriver
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

# //*[@id="divProgressIcon"]
class Listener(AbstractEventListener):
    def after_click(self, element, driver):
        print("After click")


def search_for_progress(driver):
    try:
        progress = driver.find_element_by_xpath('//*[@id="divProgressIcon"]')
        val = progress.get_attribute('style')
        print('style of element ', val)
        if progress.is_displayed():
            print('displayed')
            return True
        else:
            print('not displayed')
            return False
    except Exception as ex:
        print("element nieobecny", ex)
        return False


def main():
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    t = input('start')
    page = scrap2.page_hanlder(driver, 's')
    state = page.get_county_name()
    data = scrap2.data_handler(page, driver, state)
    i = 0
    # search_for_progress(driver)
    page.check_status()
    page.emergency_refresh()
    page.search_for_popup()
    page.check_status()
    page.search_for_popup()
    if page.wait_for_progress():
        time.sleep(1)
    page.check_status()


if __name__ == '__main__':
    main()