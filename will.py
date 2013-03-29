from bs4 import BeautifulSoup
import urllib
import urllib2
import re


def getData():
    data = parsePage("http://facilities.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01&locationName=Rockefeller+%26+Mathey+Colleges&sName=Princeton+University+Dining+Services&naFlag=1")
    #return ['will', 'test', 'data']
    return data


def parsePage(page):
    ref = urllib2.urlopen(page)
    webpage = ref.read()
    soup = BeautifulSoup(webpage)
    pt = soup.get_text()
    pattern = "Lunch"
    m = re.search(pattern, pt)
    index = -1
    fn=[]
    fn.append([])
    fn.append([])
    fn.append([])
    names =  soup.find_all('a')
    for s in names:
        if s['name'] == "Breakfast" or s['name'] == "Lunch" or s['name'] == "Dinner":
            index += 1
        else:
            fn[index].append(s.text)
    for s in fn[0]:
        print s
    return ""

getData()
