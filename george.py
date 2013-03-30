import bs4
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import string

# The dining halls we work with
hallnames = ["Butler", "Forbes", "Rockefeller", "Whitman"]
daynames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

class Dining:
	halls = []
	def html_string(self):
		s = ""
		for hall in self.halls:
			s += hall.html_string()
		return s

class Hall:
	name = ""
	link = ""
	days = []
	def html_string(self):
		s = "<h3>" + self.name + "</h3><br>"
		for day in self.days:
			s += day.html_string()
		return s
		
class Entree:
	name = ""
	ingredients = []
	allergens = []
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
	breakfast = []
	lunch = []
	dinner = []
	def string(self):
		s = ""
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
		# May not be necessary, not liked by ascii
		s.replace(u'\xa0', ' ').encode('utf-8')
		return s

def parseHomePage(root, page):
	ref = urllib2.urlopen(page)
	webpage = ref.read()
	soup = BeautifulSoup(webpage)
	pt = soup.get_text()
	links = soup.find_all('a')
	dining = Dining()
	for s in links:
		if s.string is not None:
			if any(hallname in s.string for hallname in hallnames):
				hall = Hall()
				hall.name = s.string.strip()
				hall.link = root + s['href']
				hall.days = parseHallPage(root, hall.link)
				dining.halls.append(hall)
	return dining
	
def parseHallPage(root, page):
	ref = urllib2.urlopen(page)
	webpage = ref.read()
	soup = BeautifulSoup(webpage)
	frames = soup.find_all('frame')
	days = []
	for frame in frames:
		if frame['title'] == "left navigation menu":
			dayslink = root + frame['src']
			days = parseDaysPage(root, dayslink)
	return days

def parseDaysPage(root, page):
	ref = urllib2.urlopen(page)
	webpage = ref.read()
	soup = BeautifulSoup(webpage)
	links = soup.find_all('a')
	days = []
	for link in links:
		if any(dayname in link.string for dayname in daynames):
			daylink = root + link['href']
			days.append(parseMenuPage(root, daylink))
			days[len(days)-1].date = link.string
	return days
	
def parseMenuPage(root, page):
	ref = urllib2.urlopen("http://facilities.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01&locationName=Rockefeller+%26+Mathey+Colleges&sName=Princeton+University+Dining+Services&naFlag=1")
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
		if s.text == "Top of Page":
			continue
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
	str = str.replace(u'\xa0', ' ').encode('utf-8')
	findex = 0
	bindex = len(str)
	if bindex == 0:
		return ""
	while str[findex] == " ":
		findex += 1
	while str[bindex-1] == " ":
		bindex -= 1
	return str[findex:bindex]

def getData():
	root = "http://facilities.princeton.edu/dining/_Foodpro/"
	page = "http://facilities.princeton.edu/dining/_Foodpro/location.asp"
	data = parseHomePage(root, page)
	return data

data = getData()
print "success"