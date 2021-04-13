#!/usr/bin/python

import json
import requests
from bs4 import BeautifulSoup


with open("config.json", 'r') as f:
    pay_load = json.load(f)

class udvash():
    def __init__(self):
        url = input("url:")
        if "ViewClassNote" in url:
            self.class_notes(url)
        elif "ViewRecording" in url:
            self.video(url)

    def video(self, url):
        soup = self.webpage(url)
        video_link = soup.select("#video_1 > source:nth-child(1)")[0]["src"]
        # print(video_link)
        if video_link == "":
            print("an error occurred!")
            return
        dir = input("Where to download:")
        if dir == "":
            dir = "."
        if dir[-1] != '/':
            dir = dir + "/"
        print("got video link!")
        Headers = {
            'Accept': '*/*',
            'Referer': 'https://online.udvash-unmesh.com/',
            'Connection': 'keep-alive'
        }
        fname = str(input("file name:"))
        if fname == "":
            fname = str(video_link).split('/')[-1]
        fname = dir + fname + ".mp4"
        print("downloading")
        with open(fname, 'wb') as video:
            response = requests.get(video_link, headers=Headers)
            video.write(response.content)
            print(fname, '(done!)')

    def class_notes(self, url):
        soup = self.webpage(url)
        fname = soup.select(".col-md-6")[0].text
        link = soup.select(".btn")[0]["href"]
        if link == "":
            print("an error occurred!")
            return
        dir = input("Where to download:")
        if dir == "":
            dir = "."
        if dir[-1] != '/':
            dir = dir + "/"
        fname = dir + str(fname) + ".pdf"
        print("downloading")
        response = requests.get(link)
        with open(fname, 'wb') as video:
            video.write(response.content)
            print(fname, '(done!)')
            
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


udvash()
