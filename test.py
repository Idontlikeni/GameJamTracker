from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import datetime as dt

names = []
dates = []
links = []
htm = ''
images = []
joined = []
url = 'https://itch.io/jams'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('div', class_="conversion_link_widget")
dat = soup.find_all('span', class_="date_countdown")
imag = soup.find_all('div', class_='jam_cover')
lin = soup.find_all(['div'], class_="conversion_link_widget")
jo = soup.find_all(['div'], class_="stat")
for i in imag:
    images.append(str(i).split('data-background_image="')[1].split('"')[0])
for i in quotes:
    if i.text != '':
        names.append(i.text)
for i in dat:
    if 'title' in str(i):
        ong = ''
    else:
        ong = 'Ongoing, ends: '
    time = i.text[:-1].split('T')
    datet = list(map(int, time[0].split('-')))
    my_date = dt.date(datet[0], datet[1], datet[-1])
    datet = list(map(int, time[1].split(':')))
    my_time = dt.time(datet[0], datet[1], datet[-1])
    my_datetime = dt.datetime.combine(my_date, my_time)
    delta_time1 = dt.timedelta(hours=3)
    dates.append(ong + str(my_datetime + delta_time1))
for i in lin:
    links.append(str(i).split('a href="')[1].split('"')[0])
links = links[::2]
for i in jo:
    joined.append(i.text.split()[0])

for i in range(len(names)):
    htm += f'</br><br>{names[i]}</br><img src="{images[i]}"></img></br>{dates[i]}</br><a href="https://itch.io{links[i]}">https://itch.io{links[i]}</a>'
    # print(names[i], images[i], dates[i], links[i], sep='\n')

time1 = min(dates)
indx = dates.index(time1)
name1 = names[indx]
join1 = joined[indx]
im1 = images[indx]
lin1 = f'https://itch.io{links[indx]}'
dates1 = dates[:]
dates1.remove(time1)
time2 = min(dates1)
indx = dates.index(time2)
name2 = names[indx]
join2 = joined[indx]
im2 = images[indx]
lin2 = f'https://itch.io{links[indx]}'
dates1.remove(time2)
time3 = min(dates1)
indx = dates.index(time3)
name3 = names[indx]
join3 = joined[indx]
im3 = images[indx]
lin3 = f'https://itch.io{links[indx]}'
dates1.remove(time3)
time4 = min(dates1)
indx = dates.index(time4)
name4 = names[indx]
join4 = joined[indx]
im4 = images[indx]
lin4 = f'https://itch.io{links[indx]}'
app = Flask(__name__)
time2 = time2.split()
x = time2[0].split('-')
x.reverse()
time2[0] = '.'.join(x)
time2 = ' '.join(time2)
time3 = time3.split()
x = time3[0].split('-')
x.reverse()
time3[0] = '.'.join(x)
time3 = ' '.join(time3)
time4 = time4.split()
x = time4[0].split('-')
x.reverse()
time4[0] = '.'.join(x)
time4 = ' '.join(time4)


@app.route('/')
def qwertyj():
    return render_template('index.html', time1=time1, name1=name1, join1=join1, im1=im1, lin1=lin1, lin2=lin2,
                           time2=time2, name2=name2, join2=join2, time3=time3, im2=im2, im3=im3, lin3=lin3,
                           name3=name3, join3=join3, time4=time4, name4=name4, join4=join4, im4=im4, lin4=lin4)


if __name__ == '__main__':
    app.run(port=8085, host='127.0.0.1')
