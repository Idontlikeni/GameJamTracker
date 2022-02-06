import requests
from bs4 import BeautifulSoup


link = 'https://itch.io/jams/upcoming/featured'
responce = requests.get(link).text
soup = BeautifulSoup(responce, 'html.parser')
block = soup.find_all('div', class_="jam")
for b in block:
    print(b.prettify())