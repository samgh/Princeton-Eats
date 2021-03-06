from bs4 import BeautifulSoup
import urllib3
import unicodedata
import string

class Entree:
    name = ""
    ingredients = []
    allergens = []
    def ascii(self):
        self.name = ascii(self.name)
        for i in self.ingredients:
            i = ascii(i)
        for a in self.allergens:
            a = ascii(a)
    def string(self):
        s = "Name:        "+self.name + '\n'
        s += "Ingredients: "
        for i in range(0, len(self.ingredients)):
            if i == len(self.ingredients)-1:
                s += self.ingredients[i]
            else:
                s += (self.ingredients[i]+", ")
        s += "\nAllergens:   "
        for i in range(0, len(self.allergens)):
            if i == len(self.allergens)-1:
                s += self.allergens[i]
            else:
                s += (self.allergens[i]+", ")
        s += "\n"
        return s

    def html_string(self):
        s = "Name:        "+self.name + "<br>"
        s += "Ingredients: "
        for i in range(0, len(self.ingredients)):
            if i == len(self.ingredients)-1:
                s += self.ingredients[i]
            else:
                s += (self.ingredients[i]+", ")
        s += "<br>Allergens:   "
        for i in range(0, len(self.allergens)):
            if i == len(self.allergens)-1:
                s += self.allergens[i]
            else:
                s += (self.allergens[i]+", ")
        s += "<br><br>"
        return s


class Menu:
    date = ""
    breakfast = []
    lunch = []
    dinner = []
    def ascii(self):
        self.date = ascii(self.date)
        for b in self.breakfast:
            b.ascii()
        for l in self.lunch:
            l.ascii()
        for d in self.dinner:
            d.ascii()
    def string(self):
        s = "" #self.date+"\n"
        s += "Breakfast:\n"
        s += "----------------------------------------------------------\n"
        for e in self.breakfast:
            s += e.string()
            s += "----------------------------------------------------------\n"
        s += "\nLunch:\n"
        s += "----------------------------------------------------------\n"
        for e in self.lunch:
            s += e.string()
            s += "----------------------------------------------------------\n"
        s += "\nDinner:\n"
        s += "----------------------------------------------------------\n"
        for e in self.dinner:
            s += e.string()
            s += "----------------------------------------------------------\n"
        return s
    def html_string(self):
        s = "<h3>" + self.date + "</h3>"
        s += "<h3>Breakfast:</h3>"
        for e in self.breakfast:
            s += e.html_string()
        s += "<h3>Lunch:</h3>"
        for e in self.lunch:
            s += e.html_string()
        s += "<h3>Dinner:</h3>"
        for e in self.dinner:
            s += e.html_string()
        # May not be necessary, not liked by ascii
        s.replace(u'\xa0', ' ').encode('utf-8')
        return s

def getData():
    root = "http://facilities.princeton.edu/dining/_Foodpro/"
    pool = urllib3.PoolManager()
#    data = parseMenuPage(root, "http://facilities.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01&locationName=Rockefeller+%26+Mathey+Colleges&sName=Princeton+University+Dining+Services&naFlag=1")
    data = parseMenuPage(pool, root, "http://facilities.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=02&locationName=Butler+%26+Wilson+Colleges&sName=Princeton+University+Dining+Services&naFlag=1")
    return data

def parseMenuPage(pool, root, page):
    ref = pool.request('GET', page)
    webpage = ref.data
    #print "Got a menu to parse:"
    #print "Root:", root
    #print "Page:", page
    #print "Status:", ref.status
    soup = BeautifulSoup(webpage)
    pt = soup.get_text()
    links = soup.find_all('a')
    menu = Menu()
    for s in links:
        if s['name'] == "Breakfast":
            menu.breakfast = parseMealPage(pool, root, root+s['href'])
        if s['name'] == "Lunch":
            menu.lunch = parseMealPage(pool, root, root+s['href'])
        if s['name'] == "Dinner":
            menu.dinner = parseMealPage(pool, root, root+s['href'])
    return menu

def parseMealPage(pool, root, page):
    #ref = urllib2.urlopen(page)
    #webpage = ref.read()
    ref = pool.request('GET', page)
    webpage = ref.data
    #print "Got a meal to parse"
    soup = BeautifulSoup(webpage)
    entrees = soup.find_all('a')
    ents = []
    for s in entrees[1:]:
        if s.text == "Top of Page":
            continue
        e = Entree()
        e.name = s.text
        parse = parseEntreePage(pool,root,root+ s['href'])
        e.ingredients = parse[0]
        e.allergens = parse[1]
        ents.append(e)
    return ents
    

def parseEntreePage(pool, root, page):
    ref= pool.request('GET', page)
    webpage = ref.data
    #print "Got an entree to parse"
    soup = BeautifulSoup(webpage)
    ingred = []
    allerg = []
    text =  stripSpace(soup.text)
    lines = []
    lines = text.split('\n')
    for s in lines:
        if s[:12] == "INGREDIENTS:":
            str = s[13:]
            str = string.replace(str, " (",", ")
            str = string.replace(str, ")", "")
            ingred = (str.split(','))
            # Some foods may not have ingredients, dont want a crash
            if isEmpty(ingred[0]):
                ingred = []
                continue
            for i in range(0, len(ingred)):
                ingred[i] = stripSpace(ingred[i])
        if s[:10] == "ALLERGENS:":
            allerg = (s[10:].split(','))
            # Some foods don't have allergens, causes problems
            if isEmpty(allerg[0]):
                allerg = []
                continue
            for i in range(0, len(allerg)):
                allerg[i] = stripSpace(allerg[i])
    #vals = soup.find_all('span')
    #print vals
    return [ingred, allerg]

def isEmpty(str):
    str = str.replace(u'\xa0', ' ').encode('utf-8')
    for i in range(0, len(str)):
        if str[i] != " ":
            return False
    return True

def stripSpace(str):
    if isinstance(str, unicode):
        str = unicodedata.normalize('NFKD', str).encode('ascii','ignore')
    if isinstance(str, unicode):
        print "Unicode conversion error"
    #str = str.replace(u'\xa0', ' ').encode('utf-8')
    findex = 0
    bindex = len(str)
    if bindex == 0:
        return ""
    while str[findex] == " ":
        findex += 1
    while str[bindex-1] == " ":
        bindex -= 1
    return str[findex:bindex]

def ascii(str):
    if isinstance(str, unicode):
        str = unicodedata.normalize('NFKD', str).encode('ascii','ignore')
        print str
    return str

#d = getData()
#d.ascii()
#print d.string()
