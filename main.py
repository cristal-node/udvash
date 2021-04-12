#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from pathlib import Path

personal_cookie = ''
user_agent = ''

def cls_notes(link, pp):
    rlink = "https://online.udvash-unmesh.com" + link
    headers = {
        'authority': 'online.udvash-unmesh.com',
        'user-agent': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://online.udvash-unmesh.com/Routine',
        'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
        'cookie': personal_cookie,
        'sec-gpc': '1',
    }
    response = requests.get(rlink, headers=headers)
    tsoup = BeautifulSoup(response.text, features='lxml')
    name = " ".join(tsoup.find('div', attrs={'class': 'col-md-6'}).string.split()[2:])
    url = tsoup.find('iframe').attrs['src'].split('#')[0]
    file_name = pp + '/' + name + '.pdf'
    if ( not Path(file_name).is_file() ) or ( Path(file_name).stat().st_size != int(requests.head(url, headers=headers).headers['Content-Length']) ):
        try:
            Path(file_name).unlink()
        except:
            pass
        with open(file_name, 'wb') as ff:
            ff.write(requests.get(url, headers=headers).content)
            print(name + '.pdf', '(done!)')
    else:
        print(file_name + ';  ', 'exists! (skipping)')


def video(link, pp, name):
    link = "https://online.udvash-unmesh.com" + link

    headers = {
        'authority': 'online.udvash-unmesh.com',
        'user-agent': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://online.udvash-unmesh.com/Routine',
        'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
        'cookie': personal_cookie,
        'sec-gpc': '1',
    }

    response = requests.get(link, headers=headers)
    video_soup = BeautifulSoup(response.text, features='lxml')
    vlink = video_soup.find('video').source.attrs['src']
    fname = name + '.mp4'
    name = pp + '/' + fname
    headers = {
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'video',
        'referer': link,
        'accept-language': 'en-US,en;q=0.9'
    }
    if ( not Path(name).is_file() ) or ( Path(name).stat().st_size != int(requests.head(vlink, headers=headers).headers['Content-Length']) ):
        try:
            Path(name).unlink()
        except:
            pass
        with open(name, 'wb') as video:
            video.write(requests.get(vlink, headers=headers).content)
            print(fname, '(done!)')
    else:
        print(name + ';  ', 'exists! (skipping)')







def path(parent, date, month, year):
    pp = parent + '/' + year + '/' + month + '/' + date
    Path(pp).mkdir(parents=True, exist_ok=True)
    return pp


class udvash():
    def __init__(self):
        self.load()
        root = input('Root folder:')
        with open('load.html', 'r') as load:
            soup = BeautifulSoup(load, features='lxml')
            # body = soup.find_all('a', text="Replay Video")
            test = soup.find_all('div', attrs={'class': 'uu-routine-item routineBox'})
            for el in test:
                # print(el.div.attrs['class'])
                fn = el.find('div', attrs={'class': 'uu-routine-item-head'})
                name = fn.h2.string.split()[2]
                ft = el.find('div', attrs={'class': 'uu-routine-item-body'})
                time = ft.h4.text.split()
                date = time[3]
                month = time[4][:-1]
                year = time[5]
                pth = []
                pth.append(path(root, date, month, year))
                fnt = el.find('div', attrs={'class': 'uu-routine-item-footer'}).contents[1].attrs
                if 'href' in fnt:
                    nlink = fnt['href']
                    cls_notes(nlink, pth[0])
                fv = el.find('div', attrs={'class': 'uu-routine-item-footer'}).contents
                if len(fv) >= 4:
                    vlink = fv[3].attrs['href']
                    video(vlink, pth[0], name)

    def load(self):
        headers = {
            'authority': 'online.udvash-unmesh.com',
            'accept': '*/*',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': user_agent,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://online.udvash-unmesh.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://online.udvash-unmesh.com/Routine',
            'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
            'cookie': personal_cookie,
            'sec-gpc': '1',
        }

        data = {
        'type': 'lecture',
        'courseId': '0',
        'filterType': '0',
        'lectureType': '2',
        'examPlatform': '2'
        }

        response = requests.post('https://online.udvash-unmesh.com/Routine/LoadRoutineAjax', headers=headers, data=data)
        # print(response.text)
        file = 'load.html'
        try:
            Path(file).unlink(missing_ok=True)
        except:
            pass
        with open(file, 'w') as load:
            load.write(response.text)



#if __name__ == "__main__":
#    try:
#        udvash()
#        udvash()
#        print('Please run the script again to make sure everything is fully downloaded')
#    except:
#        print('Something went wrong! Please try again')

udvash()


# udvash.load('dummy')
# cls_notes('dummy')
