import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import urllib3
import math

# setting urls split between mens/womens volleyball/swimming
volleyball_teams = {
                  'mens_volleyball': ["https://ccnyathletics.com/sports/mens-volleyball/roster", "https://lehmanathletics.com/sports/mens-volleyball/roster", "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster", "https://johnjayathletics.com/sports/mens-volleyball/roster", "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster", "https://mecathletics.com/sports/mens-volleyball/roster", "https://www.huntercollegeathletics.com/sports/mens-volleyball/roster", "https://yorkathletics.com/sports/mens-volleyball/roster"],
                  'womens_volleyball': ["https://bmccathletics.com/sports/womens-volleyball/roster", "https://yorkathletics.com/sports/womens-volleyball/roster", "https://hostosathletics.com/sports/womens-volleyball/roster", "https://bronxbroncos.com/sports/womens-volleyball/roster/2021", "https://queensknights.com/sports/womens-volleyball/roster", "https://augustajags.com/sports/wvball/roster", "https://flaglerathletics.com/sports/womens-volleyball/roster", "https://pacersports.com/sports/womens-volleyball/roster", "https://www.golhu.com/sports/womens-volleyball/roster"]
                }

swimming_teams = {
                  'mens_swimming': ["https://csidolphins.com/sports/mens-swimming-and-diving/roster/2023-2024?view=2", "https://yorkathletics.com/sports/mens-swimming-and-diving/roster", "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster", "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster", "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster", "https://mckbearcats.com/sports/mens-swimming-and-diving/roster", "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster", "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster", "https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22", "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22"],
                  'womens_swimming': ["https://csidolphins.com/sports/womens-swimming-and-diving/roster", "https://queensknights.com/sports/womens-swimming-and-diving/roster", "https://yorkathletics.com/sports/womens-swimming-and-diving/roster", "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim", "https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster", "https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster", "https://mckbearcats.com/sports/womens-swimming-and-diving/roster", "https://ramapoathletics.com/sports/womens-swimming-and-diving/roster", "https://keanathletics.com/sports/womens-swimming-and-diving/roster", "https://oneontaathletics.com/sports/womens-swimming-and-diving/roster"]
                }

#webscraping function per team
def scrape_team(url):

  headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive'
  }

  # making a request to the server
  page = requests.get(url, headers=headers)
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  names = []
  heights = []

  # Check if the connection is successful put exception later
  if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')

  # Find all td tags with names and heights
    name_tags = soup.find_all('td', class_='sidearm-table-player-name')
    raw_heights = soup.find_all('td', class_='height')

  # Extracting the names from name_tags
    for name_tag in name_tags:
      names.append(name_tag.get_text().strip())

  # Extracting the heights from the raw heights and split the string by text '-'
    for height in raw_heights:
      adhoc_heights = height.get_text().split('-')

  # if there's a missing value, put nan
      if len(adhoc_heights) > 1 and adhoc_heights[0] and adhoc_heights[1]:
        feet = int(adhoc_heights[0]) * 12
        inch = int(adhoc_heights[1])
        height_inches = feet + inch

      else:
        height_inches = math.nan

    # append the values to a list
      heights.append(height_inches)

  return names, heights

volleyball_men_names, volleyball_men_heights = [], []
volleyball_women_names, volleyball_women_heights = [], []
swimming_men_names, swimming_men_heights = [], []
swimming_women_names, swimming_women_heights = [], []

# Volleyball loop
for gender, urls in volleyball_teams.items():

  for url in urls:
    names, heights = scrape_team(url)

    if gender == 'mens_volleyball':
      volleyball_men_names.extend(names)
      volleyball_men_heights.extend(heights)

    elif gender == 'womens_volleyball':
      volleyball_women_names.extend(names)
      volleyball_women_heights.extend(heights)

# Swimming loop
for gender, urls in swimming_teams.items():

  for url in urls:
    names, heights = scrape_team(url)

    if gender == 'mens_swimming':
      swimming_men_names.extend(names)
      swimming_men_heights.extend(heights)

    elif gender == 'womens_swimming': 

volleyball_players_df = pd.DataFrame({
    'Men_name':   pd.Series(volleyball_men_names),
    'Men_height': pd.Series(volleyball_men_heights),
    'Women_name': pd.Series(volleyball_women_names),
    'Women_height': pd.Series(volleyball_women_heights)
})

swimming_players_df = pd.DataFrame({
    'Men_name':   pd.Series(swimming_men_names),
    'Men_height': pd.Series(swimming_men_heights),
    'Women_name': pd.Series(swimming_women_names),
    'Women_height': pd.Series(swimming_women_heights)
})

# drops NaN
men_swim = swimming_players_df[["Men_name", "Men_height"]].dropna()
women_swim = swimming_players_df[["Women_name", "Women_height"]].dropna()
men_vball = volleyball_players_df[["Men_name", "Men_height"]].dropna()
women_vball = volleyball_players_df[["Women_name", "Women_height"]].dropna()

men_swim.to_csv("men_swimming.csv", index=False)
women_swim.to_csv("women_swimming.csv", index=False)
men_vball.to_csv("men_volleyball.csv", index=False)
women_vball.to_csv("women_volleyball.csv", index=False)



