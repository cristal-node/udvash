#!/usr/bin/python

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

with open("config.json", 'r') as f:
    pay_load = json.load(f)



def path(parent, date, month, year):
    pp = parent + '/' + year + '/' + month + '/' + date
    Path(pp).mkdir(parents=True, exist_ok=True)
    return pp


class udvash():
    def __init__(self):
        # root = input('Root folder:')
        root = ""
        soup = self.Routine()
        items = soup.select("div.col-md-4")
        for item in items:
            d = self.item(item, root)
            if len(item.select("a")) > 0:
                base = "https://online.udvash-unmesh.com"
                note_link = base + item.select("a")[0]['href']
                video_link = base + item.select("a")[1]['href']
                print(note_link, video_link, "********88")
                self.cls_notes(note_link, d['path'])
                self.video(video_link, d['path'], d['name'])

    def Routine(self):
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': '*/*',
            'Referer': 'https://online.udvash-unmesh.com/Routine',
            'Origin': 'https://online.udvash-unmesh.com'
        }

        data = {
        'type': 'lecture',
        'courseId': '0',
        'filterType': '0',
        'lectureType': '2',
        'examPlatform': '2'
        }

        response = requests.post('https://online.udvash-unmesh.com/Routine/LoadRoutineAjax', headers=Headers, data=data)
        soup = BeautifulSoup(response.text, features='lxml')
        return soup

    def webpage(self, url):
        print("Fetching data")
        Headers = {
            'User-Agent': pay_load[0]["user_agent"],
            'Accept': '*/*',
            'Referer': 'https://online.udvash-unmesh.com/Routine'
        }

        response = requests.get(url, headers=Headers, cookies=pay_load[1])
        soup = BeautifulSoup(response.text, features='lxml')
        return soup

    def item(self, item, root):
        d = {}
        d['name'] = "".join(item.select("h2.uu-routine-title")[0].text.split()[2:])
        time = item.select("h4")[0].text.split()
        date = time[3]
        month = time[4][:-1]
        year = time[5]
        d['path'] = path(root, date, month, year)
        return d

    def video(self, link, pp, name):
        soup = self.webpage(link)
        video_link = soup.select("#video_1 > source:nth-child(1)")[0]["src"]
        fname = name + '.mp4'
        name = pp + '/' + fname
        Headers = {
            'Accept': '*/*',
            'Referer': link,
            'Connection': 'keep-alive'
        }
        if ( not Path(name).is_file() ) or ( Path(name).stat().st_size != int(requests.head(video_link, headers=Headers).headers['Content-Length']) ):
            try:
                Path(name).unlink()
            except:
                pass
            with open(name, 'wb') as video:
                video.write(requests.get(video_link, headers=Headers).content)
                print(fname, '(done!)')
        else:
            print(name + ';  ', 'exists! (skipping)')

    def cls_notes(self, link, pp):
        soup = self.webpage(link)
        name = soup.select(".col-md-6")[0].string.split()[2:]
        url = soup.select(".btn")[0]["href"]
        file_name = pp + '/' + name + '.pdf'
        if ( not Path(file_name).is_file() ) or ( Path(file_name).stat().st_size != int(requests.head(url).headers['Content-Length']) ):
            try:
                Path(file_name).unlink()
            except:
                pass
            with open(file_name, 'wb') as ff:
                ff.write(requests.get(url).content)
                print(name + '.pdf', '(done!)')
        else:
            print(file_name + ';  ', 'exists! (skipping)')




if __name__ == "__main__":
   try:
       udvash()
       print('Please run the script again to make sure everything is fully downloaded')
   except:
       print('Something went wrong! Please try again')