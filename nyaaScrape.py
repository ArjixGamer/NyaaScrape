from bs4 import BeautifulSoup as bs
import requests
import urllib
import re
import os
import subprocess
import sys

def userSelection():
    cataChecker = input("Anime or Manga \n")
    if cataChecker == 'Anime' or cataChecker == 'anime' or cataChecker == 'a':
        search = showCheck()
        filt = filterCheck()
        ud = udCheck()
        link = f'https://nyaa.si/?q={search}&f=0&c=1_2&s={filt}&o={ud}'
        return link
    elif cataChecker == 'Manga' or cataChecker == 'manga' or cataChecker == 'm':
        search = showCheck()
        filt = filterCheck()
        ud = udCheck()
        link = f'https://nyaa.si/?q={search}&f=0&c=3_1&s={filt}&o={ud}'
        return link
    else:
        raise Exception("Please insert anime or manga!")
        
def filterCheck():
    filta = ['size','seeders','id']
    ud = ['asc','desc']
    filt = input("Filter by Size (0), Seeders (1), Date (2) \n")
    if int(filt) < 3 and int(filt) > -1:
        return filta[int(filt)]
    else:
        raise Exception("Please use the correct selections!")
        
def udCheck():
    ud = ['desc','asc']
    choice = input("Descending (0) or Ascending? (1) \n")
    if int(choice) < 2 and int(choice) > -1:
        return ud[int(choice)]
    else:
        raise Exception("Please use the correct selections!")

def showCheck():
    search = input("What do you want to search for? \n")
    return search

def torrentDownloader(magnet,inOrout):
    if inOrout == 'Y' or inOrout == 'y':
        os.startfile(magnet)
    else:
        def run_command(magnet):
            process = subprocess.Popen(f'aria2c {magnet}', stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print (output.strip())
            rc = process.poll()
            return rc
        run_command(magnet)
        

def searchResults():
    Storage = [
        SearchResult(
        title = i.select("a:not(.comments)")[1].get("title"),
        size = i.find_all('td',class_ = 'text-center')[1].text,
        seeders = i.find_all('td',class_= 'text-center')[3].text,
        leechers = i.find_all('td',class_ = 'text-center')[4].text,
        magnet = i.find_all('a',{'href':re.compile(regex)})[0].get('href'))
        for i in lol.select("tr.default, tr.success")
    ]
    return Storage

class SearchResult:
    def __init__(self, title, size, seeders, leechers, magnet, poster='', meta=''):
        self.title = title
        self.magnet = magnet
        self.size = size
        self.leechers = leechers
        self.seeders = seeders
        self.poster = poster
        self.meta = meta

    def __repr__(self):
        return '<SearchResult Title: {} Size: {} Seeders: {} Leechers: {} Magnet: {}>'.format(self.title, self.size,
                                                                                            self.seeders,
                                                                                            self.leechers,
                                                                                            self.magnet)
    def __str__(self):
        return self.title

    @property
    def pretty_metadata(self):
        """
        pretty_metadata is the prettified version of metadata
        """
        if self.meta:
            return ' | '.join(val for _, val in self.meta.items())
        return ''

if __name__ == '__main__':
    regex = r'(magnet:)+[^"]*'
    Link = userSelection()
    page = requests.get(Link).text
    lol = bs(page, 'html.parser')
    Storage = searchResults()
    for i in range(len(Storage)):
        print(i, ' ', Storage[i], '\n',
              Storage[i].size, '\n',
              'Seeders', Storage[i].seeders )
    choice = input('Which one would you like to select? \n')
    inOrout = input('Would you like to use an external torrent handler? [Y,n] \n')
    magnet = Storage[int(choice)].magnet
    torrentDownloader(magnet,inOrout)
    print('Download has completed.')
