from selenium import webdriver
import pandas as pd
import time
import math

flat_types = {
    '1+kt': 1,
    '1+1': 2,
    '2+kt': 3,
    '2+1': 4,
    '3+kt': 5,
    '3+1': 6,
    '4+kt': 7,
    '4+1': 8,
    '5+kt': 9,
    '5+1': 10,
    'flatshare': 11,
    'unusual': 12
}

regions = {
    'Praha 1': 1,
    'Praha 2': 2,
    'Praha 3': 3,
    'Praha 4': 4,
    'Praha 5': 5,
    'Praha 6': 6,
    'Praha 7': 7,
    'Praha 8': 8,
    'Praha 9': 9,
    'Praha 10': 10,
    'Praha 11': 11
}

page = 1
url = 'https://www.sreality.cz/en/search/to-rent/apartments/praha?page='
page_selector = '#page-layout > div.content-cover > div.content-inner > div.transcluded-content.ng-scope > div > div > div' \
                '> div > div:nth-child(4) > div > div.paging.ng-scope > p > span:nth-child(2)'

# Selenium settings
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)

driver.get(url + str(page))
flats_in_total = int(driver.find_element_by_css_selector(
).text.replace(
    ' ', ''))

flats = pd.DataFrame(columns=['type', 'size', 'locality', 'price'])

total_pages = math.ceil((flats_in_total - 1) / 20)

for i in range(0, total_pages):
    driver.get(url + str(page + i))
    flat_info = driver.find_elements_by_css_selector('.info .text-wrap')

    for el in flat_info:
        flat = el.text.split('\n')
        flat_size = int(flat[0].split(' ')[len(flat[0].split(' ')) - 2])
        flat_type = ''
        flat_locality = ''

        if 'Information about price at agency' in flat[2]:
            flat_price = None
        else:
            flat_price = int(flat[2].split('CZK')[0].replace(' ', ''))

        for key in flat_types.keys():
            if key in flat[0]:
                flat_type = flat_types[key]

        for key in regions.keys():
            if key in flat[1]:
                flat_locality = regions[key]

        if flat_locality == '':
            flat_locality = 0

        flats.loc[len(flats)] = [flat_type, flat_size, flat_locality, flat_price]

    time.sleep(1)

flats.to_csv('flats_info.csv')

driver.quit()
