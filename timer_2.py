async def top(self, count, secs):
        data1 = []
        while True:
            names = []
            dates = []
            links = []
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
            data = []
            for i in range(len(names)):
                data.append((names[i], dates[i], links[i], images[i], int(''.join(joined[i].split(',')))))
            for i in data:
                if 'Ongoing' in i[1]:
                    data.remove(i)
            data = sorted(data, key=lambda student: student[-1])
            data.reverse()
            data = data[:count]
            if data1:
                if data != data1:
                    for i in range(count):
                        if data[i] != data1[i]:
                            data[i] = ''
                    for i in data1:
                        if i in data:
                            data1.remove(i)
                    for i in range(count):
                        if data[i] == '':
                            data[i] = data1[0]
                            data1 = data1[1:]
            for i in data:
                print(i)
            data1 = data[:]
            await asyncio.sleep(secs)
            print()