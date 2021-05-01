from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
import sys
import time
import pandas as pd 
import xlsxwriter
import threading
from pynput.keyboard import Listener, KeyCode, Key
from pynput.mouse import Button, Listener
from pynput.mouse import Controller as mouseController
from pynput.keyboard import Controller as keyController 
import pyautogui



def empty_page(driver):
    try:
        message = driver.find_element_by_xpath('//*[@id="divInfoKomunikat"]').text
        if message == 'Nie znaleziono podmiotów.':
            return True
    except:
        return False

def change_page():
    mouse = mouseController()
    pyautogui.moveTo(658, 502)
    mouse.click(Button.left)
    


def change_street():
    mouse = mouseController()
    keyboard = keyController()
    pyautogui.moveTo(427, 669) #street view
    mouse.click(Button.left)
    
    time.sleep(1)
    
    keyboard.press(Key.down)
    keyboard.release(Key.down)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    pyautogui.moveTo(440, 790)
    time.sleep(0.25)
    mouse.click(Button.left)

def change_town():
    mouse = mouseController()
    keyboard = keyController()
    pyautogui.moveTo(404, 642) #town view
    mouse.click(Button.left)
    time.sleep(1)
    keyboard.press(Key.down)
    keyboard.release(Key.down)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    pyautogui.moveTo(440, 790)
    time.sleep(0.25)
    mouse.click(Button.left)

def check_status(driver, mode):
    print('checking status')
    element = driver.find_element_by_xpath('//*[@id="spanPageIndex"]').text
    result = element.split('/')
    if empty_page(driver):
        if mode == 's':
            change_street()
        elif mode == 't':
            change_town()
        else:
            print('wrong mode')
    else:
        if len(result) == 1:
            print('empty')
            if mode == 's':
                print('change street')
                change_street()
            elif mode == 't':
                print('change town')
                change_town()
            else:
                print('wrong mode')
        else:
            if int(result[0]) < int(result[1]):
                print(result[0])
                print('next page')
                change_page()
            else:
                if mode == 's':
                    print('next street')
                    change_street()
                elif mode == 't':
                    print('next town')
                    change_town()
                else:
                    print('wrong mode')

def write_to_file(companies_list):
    df = pd.DataFrame(companies_list)
    writer = pd.ExcelWriter('output1.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1')
    writer.save()


def making_item(companies_list, rows):
    i = 1
    for row in rows: 
                regon = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[1]' % i).text
                type = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[2]' %i).text
                name = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[3]' % i).text
                state = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[4]' % i).text
                county = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[5]' % i).text
                community = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[6]' % i).text
                postalCode = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[7]' % i).text
                city = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[8]' % i).text
                street = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[9]' % i).text
                deleted = row.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]/td[10]' % i).text
                i += 1
                item = {'Regon': regon, 'Typ': type, 'Nazwa': name, 'Województwo': state, 'Powiat': county, 'Gmina': community, 
                "Kod Pocztowy": postalCode, 'Miasto': city, 'Ulica': street, 'Informacja u usniętym wpisie': deleted}
                companies_list.append(item)        
    print('DONE')
    
def count_rows(driver):
    rows = []
    element = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[1]')
    num = 2
    while(True):
                rows.append(element)
                try:
                    element = driver.find_element_by_xpath('//*[@id="divListaJednostek"]/table/tbody/tr[%d]' %num)
                    num += 1
                except:
                    break
    return rows


def main():    
    companies_list = []
    url = 'https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx'
    driver = webdriver.Chrome()
    driver.get(url)
    # time.sleep(90)
    mode = input("Type s for street change, t for town change ")
    check_tab = count_rows(driver)
    making_item(companies_list, check_tab)
    check_status(driver, mode)
    while True:  
        try:
            if empty_page(driver):
                check_status(driver, mode)    
            rows = count_rows(driver)
            if rows != check_tab:       
                making_item(companies_list, rows)
                check_tab = rows
                del(rows)
                check_status(driver, mode)
            else:
                print("Waiting")
                time.sleep(1)
            
        except KeyboardInterrupt:
            write_to_file(companies_list)
            print('bye bye')
            exit()
        except NoSuchElementException:
           print("No element exepction")
           continue
        except StaleElementReferenceException:
            continue
        except NoSuchWindowException:
            write_to_file(companies_list)
            print('\nbye bye')
            exit()
        except:
            write_to_file(companies_list)
            print('\nbye bye')
            exit()

if __name__ == '__main__':
    main()