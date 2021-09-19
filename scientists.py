from selenium import webdriver

def row_creator(web_driver) -> dict:
    output = {}
    last_key = None
    block = web_driver.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div')
    split_items = block[0].text.split('\n')
    for item in split_items:
        ready_item = item.rstrip('\n')
        if ready_item in ('Profesor', 'Doktorat', 'Habilitacja'):
            output[ready_item] = {}
            last_key = ready_item
        elif ready_item not in ('Profesor', 'Doktorat', 'Habilitacja', 'STOPNIE I TYTUŁY', '(Mniej)'):
            split_items = ready_item.split(':')
            # print('checking ', split_items, ' ', type(split_items))
            if len(split_items) > 1:     
                output[last_key][split_items[0]] = split_items[1]
            else:
                output['test'] = {}
                output['test']['unkonwn'] = split_items[0]
        else:
            continue
    return output


def main():
    driver = webdriver.Chrome()
    driver.get('https://nauka-polska.pl/#/profile/scientist?id=27951&_k=iid8du')
    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[1]/main/section/section/section[2]/div/div/div/section/div/div[3]/a').click()
    start = input('start ')
    print(row_creator(driver))
    driver.close()

if __name__ == '__main__':
    main()
