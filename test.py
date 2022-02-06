from flask import Flask
import requests
from bs4 import BeautifulSoup
import datetime as dt

names = []
dates = []
links = []
htm = ''
images = []
url = 'https://itch.io/jams'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('div', class_="conversion_link_widget")
dat = soup.find_all('span', class_="date_countdown")
imag = soup.find_all('div', class_='jam_cover')
lin = soup.find_all(['div'], class_="conversion_link_widget")
for i in imag:
    images.append(str(i).split('data-background_image="')[1].split('"')[0])
for i in quotes:
    if i.text != '':
        names.append(i.text)
for i in dat:
    if 'title' in str(i):
        time = i.text[:-1].split('T')
        datet = list(map(int, time[0].split('-')))
        my_date = dt.date(datet[0], datet[1], datet[-1])
        datet = list(map(int, time[1].split(':')))
        my_time = dt.time(datet[0], datet[1], datet[-1])
        my_datetime = dt.datetime.combine(my_date, my_time)
        delta_time1 = dt.timedelta(hours=3)
        dates.append(my_datetime + delta_time1)
    else:
        dates.append('Ongoing')
for i in lin:
    links.append(str(i).split('a href="')[1].split('"')[0])
links = links[::2]

for i in range(len(names)):
    htm += f'</br><br>{names[i]}</br><img src="{images[i]}"></img></br>{dates[i]}</br><a href="https://itch.io{links[i]}">https://itch.io{links[i]}</a>'
    # print(names[i], images[i], dates[i], links[i], sep='\n')


app = Flask(__name__)


@app.route('/')
def qwertyj():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                    <title>123</title>
                  </head>
                  <body>
                    {htm}
                  </body>
                </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
