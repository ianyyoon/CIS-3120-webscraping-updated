import requests   #requests to websites
from bs4 import BeautifulSoup  #cleans html/lets search tags
import pandas as pd   #dataframes/maniputlation/etc
import unicodedata     #lets us work with unicode

url = 'https://www.worldometers.info/world-population/population-by-country/'  #world pops website to pull data

page = requests.get(url)

if page.status_code != 200:
  return "page error"

soup = BeautifulSoup(page.content, 'html.parser')

rows = soup.find_all('tr')[1:]

print(len(rows))

country = []

for row in rows:
  td_tags = row.find('a', class_="transition-all duration-200 text-lime-600 hover:text-lime-500").get_text()
  country.append(td_tags)

print(country)

rows[0].find_all('td')[2].get_text()

population = []
year_change =[]
net_change =[]
dencity =[]
land_area =[]
migrants =[]
fert_rate=[]
median_age=[]
urban_pop=[]
world_share=[]

for row in rows:
  td_tag = row.find_all('td')

  if len(td_tag)==12:
    population.append(td_tag[2].get_text())
  year_change.append(td_tag[3].get_text())
  net_change.append(td_tag[4].get_text())
  dencity.append(td_tag[5].get_text())
  land_area.append(td_tag[6].get_text())
  migrants.append(td_tag[7].get_text())
  fert_rate.append(td_tag[8].get_text())
  median_age.append(td_tag[9].get_text())
  urban_pop.append(td_tag[10].get_text())
  world_share.append(td_tag[11].get_text())



saving_data = {
              'Country(or dependency)': country,
              'Population 2025': population,
              'Yearly Change': year_change,
              'Net Change': net_change,
              'Density(P/km^2)': dencity,
              'Land Area(Km^2)': land_area,
              'Migrants(net)' : migrants,
              'Fert. Rate': fert_rate,
              'Median Age': median_age,
              'Urban Pop%': urban_pop,
              'World Share': world_share
}

df1 = pd.DataFrame(saving_data)


df1.head()

df1.describe()

df1.info()



