import os
import sys
import urllib.parse
import csv
import urllib
import urllib.request
import re
from urllib import parse
from bs4 import BeautifulSoup

sys.setrecursionlimit(5000)
MAX_MOVIES = 3000

counter = 0
url ="http://www.torec.net/sub.asp?sub_id=323" #323" #705"

os.remove("index.csv")
#os.removedirs("data")

if not os.path.exists("data/"):
    os.makedirs("data/")

def mineData(urlM):
    global counter

    indexW = open("index.csv", "a+" ,encoding='UTF16')
    csv.writer(indexW, delimiter='\t', quotechar=',', quoting=csv.QUOTE_MINIMAL)

    reader = open("index.csv", "r", encoding='UTF16')
    indexR = csv.reader(reader)

    for row in indexR:
        if row[0].split('\t')[0] == urlM.split('=')[1]:
            return

    counter += 1
    print(counter)

    request = urllib.request.Request(urlM)
    page = urllib.request.urlopen(request).read()
    type(page)
    soup=BeautifulSoup(page, 'html.parser')

    # id
    indexW.write(urlM.split('=')[1]+'\t')

    # link
    indexW.write(urlM+'\t')

    # title
    for a in soup.findAll(attrs={'class' : 'line sub_title'}):
        indexW.write(a.contents[0].getText()+'\t')

    # year
    for a in soup.findAll(attrs={'class': 'sub_name_span'}):
        y = str(a)
        x = re.findall("[0-9]+", y)
        indexW.write(x[0]+'\t')

    # description
    for a in soup.findAll(attrs={'class': 'sub_name_div'}):
        file = open("data/" + urlM.split('=')[1] + ".txt", "w", encoding='UTF8')  # utf-8')
        if len(str(a.getText()))==0 or a.getText()==' ' or a.getText()=='':
            nextNode = a
            while True:
                nextNode = nextNode.next
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = "exit"

                if tag_name == None:
                    t = str(nextNode)
                    file.write(t)
                elif tag_name == 'br':
                    continue
                else:
                    break
        else:
            file.write(a.getText()+"\n")

        file.close()

    # actors
    for a in soup.findAll('a'):
        if len(a['href'].split('/'))>1 and a['href'].split('/')[1]=="person":
            t = a['href'].split('/')[2]
            indexW.write(t.replace('_', ' ')+', ')

    indexW.write("\n")

    indexW.close()
    reader.close()

    for a in soup.findAll('a'):
        if len(a['href'].split('/')) > 1 and a['href'].split('/')[1] == "person":
            if counter < MAX_MOVIES:
                getMovies("http://www.torec.net" + parse.quote(a['href']))
## end mineData


def getMovies(urlA):
    newMovie = True

    index = open("index.csv", "r", encoding='UTF16')
    reader = csv.reader(index)

    request = urllib.request.Request(urlA)
    page = urllib.request.urlopen(request).read()
    type(page)
    soup = BeautifulSoup(page, 'html.parser')
    global counter
    for a in soup.findAll('a'):

        if len(a['href'].split('.')) > 1 and a['href'].split('.')[0] == "/sub" and counter < MAX_MOVIES:
            for row in reader:
                if ((a['href'].split('=')[1]) == (row[0].split('\t')[0])):
                    newMovie = False
                    break

            if newMovie:
                mineData("http://www.torec.net" + a['href'])

        newMovie = True

    index.close()
## end getMovie

mineData(url)