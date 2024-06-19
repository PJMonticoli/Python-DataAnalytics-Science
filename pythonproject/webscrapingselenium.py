from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]

path = 'D:\Archivos\Escritorio\chrome-win64\chrome.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)


def get_missing_matches(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    driver.get(web)

    # xpath nodo padre //tr[contains(@style, "font-size:90%")]
    matches = driver.find_elements(
        by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find_element(by='xpath', value='./td[1]'))
        score.append(match.find_element(by='xpath', value='./td[2]'))
        away.append(match.find_element(by='xpath', value='./td[3]'))

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    time.sleep(2)
    return df_football


# Lista de comprension
missing_matches = [get_missing_matches(year) for year in years]
df_missing_matches = pd.concat(missing_matches, ignore_index=True)

driver.quit()

df_missing_matches.to_csv("missing_data.csv")
