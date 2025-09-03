import requests   #requests to websites
from bs4 import BeautifulSoup  #cleans html/lets search tags
import pandas as pd   #dataframes/maniputlation/etc
import re #used for regex cleaning

#pulling website
url = 'https://www.worldometers.info/world-population/population-by-country/'  

#Faking a browser session
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

page = requests.get(url, headers=headers, timeout=20)

#check if page loaded correctly
page.raise_for_status()

soup = BeautifulSoup(page.content, "html.parser")
rows = soup.find_all('tr')[1:]

#pull row names
header = [cell.text.strip() for cell in soup.select("table#example2 thead th")[1:]]

lists = []

#pull data from rows
for row in rows:
  columns = [cell.text.strip() for cell in row.find_all("td")]
  #Cleaning the data
  lists.append(
     [columns[0]] + [
        pd.to_numeric(re.sub("[,%+]", "", value).strip(), errors="coerce")
        for value in columns[1:]
     ]
  )
#create dataframe
df = pd.DataFrame(lists, columns=header)

df.head()





