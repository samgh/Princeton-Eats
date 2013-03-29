import bs4
from bs4 import BeautifulSoup
import urllib
import urllib2
import re

class Entree:
    name = ""
    ingredients = []
    allergens = []
    def string(self):
        s = "Name:"+self.name + '\n'
        s += "Ingredients:"
        for i in self.ingredients:
            s += (i+",")
        s += "\nAllergens:"
        for a in self.allergens:
            s += (a+",")
        s += "\n"
        return s

    def html_string(self):
        s = "Name:"+self.name + "<br>"
        s += "Ingredients:"
        for i in self.ingredients:
            s += (i+",")
        s += "<br>Allergens:"
        for a in self.allergens:
            s += (a+",")
        s += "<br><br>"
        return s


class Menu:
    breakfast = []
    lunch = []
    dinner = []
    def string(self):
        s = ""
        s += "Breakfast:\n"
        for e in self.breakfast:
            s += e.html_string()
            s += "Lunch:\n"
        for e in self.lunch:
            s += e.html_string()
            s += "Dinner:\n"
        for e in self.dinner:
            s += e.html_string()
        return s
    def html_string(self):
        s = ""
        s += "<h3>Breakfast:</h3>"
        for e in self.breakfast:
            s += e.html_string()
        s += "<h3>Lunch:</h3>"
        for e in self.lunch:
            s += e.html_string()
        s += "<h3>Dinner:</h3>"
        for e in self.dinner:
            s += e.html_string()
        s.replace(u'\xa0', ' ').encode('utf-8')
        return s

def getData():
    root = "http://facilities.princeton.edu/dining/_Foodpro/"
    data = parseMenuPage(root, "http://facilities.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01&locationName=Rockefeller+%26+Mathey+Colleges&sName=Princeton+University+Dining+Services&naFlag=1")
    #return ['will', 'test', 'data']
    return data


def parseMenuPage(root, page):
    ref = urllib2.urlopen(page)
    webpage = ref.read()
    soup = BeautifulSoup(webpage)
    pt = soup.get_text()
    links = soup.find_all('a')
    menu = Menu()
    for s in links:
        if s['name'] == "Breakfast":
            menu.breakfast = parseMealPage(root, root+s['href'])
        if s['name'] == "Lunch":
            menu.lunch = parseMealPage(root, root+s['href'])
        if s['name'] == "Dinner":
            menu.dinner = parseMealPage(root, root+s['href'])
    return menu

def parseMealPage(root, page):
    ref = urllib2.urlopen(page)
    webpage = ref.read()
    soup = BeautifulSoup(webpage)
    entrees = soup.find_all('a')
    ents = []
    for s in entrees[1:]:
        e = Entree()
        e.name = s.text
        parse = parseEntreePage(root,root+ s['href'])
        e.ingredients = parse[0]
        e.allergens = parse[1]
        ents.append(e)
    return ents
    

def parseEntreePage(root, page):
    ref = urllib2.urlopen(page)
    webpage = ref.read()
    soup = BeautifulSoup(webpage)
    ingred = []
    allerg = []
    text =  soup.text
    lines = []
    lines = text.split('\n')
    for s in lines:
        if s[:12] == "INGREDIENTS:":
            ingred = (s[13:].split(','))
        if s[:10] == "ALLERGENS:":
            allerg = (s[10:].split(','))
    #vals = soup.find_all('span')
    #print vals
    return [ingred, allerg]

