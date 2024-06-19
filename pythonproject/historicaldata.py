from bs4 import BeautifulSoup
import requests
import pandas as pd


years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]


def get_matches(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    # request para obtener el contenido HTML de la página
    response = requests.get(web)
    content = response.text
    # Aquí uso 'lxml' como parser HTML
    soup = BeautifulSoup(content, 'lxml')  # pip install lxml

    # Patron para extraer información de las filas de partidos.
    matches = soup.find_all('div', class_='footballbox')
    # Creo listas para almacenar local,resultado,vistante
    home = []
    score = []
    away = []
    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())
        score.append(match.find('th', class_='fscore').get_text())
        away.append(match.find('th', class_='faway').get_text())

    # creo un diccionario con las listas
    dict_football = {'home': home, 'score': score, 'away': away}
    # creo un dataframe con el diccionario previamente creado
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year  # nueva columna year
    return df_football


# En vez de hacer esto
# for year in years:
#     get_matches(year)
# Creo una Lista de comprensión 'fifa' para recopilar datos de varios Mundiales
fifa = [get_matches(year) for year in years]


# concateno la data de todos los mundiales en solamente un df
df_fifa = pd.concat(fifa, ignore_index=True)
# Exporto el df a csv sin el index
df_fifa.to_csv('fifa_worldcup_historical_data.csv', index=False)


df_fixture = get_matches('2022')
df_fixture.to_csv('fifa_worldcup_fixture.csv', index=False)
