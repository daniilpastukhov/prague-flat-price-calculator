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

prague_regions = {
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
    'Praha 11': 11,
    'Praha 12': 12,
    'Praha 13': 13,
    'Praha': 0
}

brno_regions = {
    'Brno - Jundrov': 1,
    'Brno - Medlánky': 2,
    'Brno - Trnitá': 3,
    'Brno - Maloměřice': 4,
    'Brno - Žabovřesky': 5,
    'Brno - Bohunice': 6,
    'Brno - Staré Brno': 7,
    'Brno - Černovice': 8,
    'Brno - Černá Pole': 9,
    'Brno - Kohoutovice': 10,
    'Brno - Pisárky': 11,
    'Brno - Líšeň': 12,
    'Brno - Královo Pole': 13,
    'Brno - Bystrc': 14,
    'Brno - Komín': 15,
    'Brno - Veveří': 16,
    'Brno - Židenice': 17,
    'Brno - Zábrdovice': 18,
    'Brno - Komárov': 19,
    'Brno - Obřany': 20,
    'Brno - Horní Heršpice': 21,
    'Brno - Nový Lískovec': 22,
    'Brno - Ponava': 23,
    'Brno - Štýřice': 24,
    'Brno - Ivanovice': 25,
    'Brno - Řečkovice': 26,
    'Brno - Husovice': 27,
    'Brno - Lesná': 28,
    'Brno - část obce Veveří': 29,
    'Brno - Brno-Komín': 30,
    'Brno - Brno-střed': 31,
    'Brno - Brno-město': 32,
    'Brno': 0
}


def get_data(url, city, regions, file_name, only_nums=False):
    page = 1
    page_selector = '#page-layout > div.content-cover > div.content-inner > div.transcluded-content.ng-scope > div > div > div' \
                    '> div > div:nth-child(4) > div > div.paging.ng-scope > p > span:nth-child(2)'

    # Selenium settings
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    driver = webdriver.Firefox(firefox_profile=firefox_profile)

    driver.get(url + str(page))
    flats_in_total = int(driver.find_element_by_css_selector(page_selector).text.replace(' ', ''))

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

            if 'Information about price at agency' in flat[2] or 'Information about price on request' in flat[2]:
                flat_price = None
            else:
                flat_price = int(flat[2].split('CZK')[0].replace(' ', ''))

            for key in flat_types.keys():  # Get flat type
                if key in flat[0]:
                    if only_nums: flat_type = flat_types[key]
                    else: flat_type = key
                    break

            for key in regions.keys():  # Get flat location
                if key in flat[1]:
                    if only_nums: flat_locality = regions[key]
                    else: flat_locality = key
                    break
                if only_nums: flat_locality = 0
                else: flat_locality = city

            flats.loc[len(flats)] = [flat_type, flat_size, flat_locality, flat_price]

        time.sleep(1)

    flats.to_csv(file_name, index=False)

    driver.quit()


prague_url = 'https://www.sreality.cz/en/search/to-rent/apartments/praha?page='
brno_url = 'https://www.sreality.cz/en/search/to-rent/apartments/jihomoravsky-kraj?region=municipality%20Brno&region-id=5740&region-type=municipality&page='

get_data(prague_url, 'Prague', prague_regions, 'flats_prague_numeric.csv')
get_data(brno_url, 'Brno', brno_regions, 'flats_brno_numeric.csv')