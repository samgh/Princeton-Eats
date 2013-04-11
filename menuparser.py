import bs4
from bs4 import BeautifulSoup
import urllib
import urllib2
import urllib3
import re
import string
import menuscraper
import unicodedata

# The dining halls we work with
hallnames = ["Butler", "Forbes", "Rockefeller", "Whitman"]
daynames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

class Dining:
	halls = []
	def ascii(self):
		for hall in self.halls:
			hall.ascii()
	def html_string(self):
		s = ""
		for hall in self.halls:
			s += hall.html_string()
		return s

class Hall:
	name = ""
	link = ""
	days = []
	def ascii(self):
		self.name = menuscraper.ascii(self.name)
		self.link = menuscraper.ascii(self.link)
		for day in self.days:
			day.ascii()
	def html_string(self):
		s = "<h3>" + self.name + "</h3><br>"
		for day in self.days:
			s += day.html_string()
		return s

def parseHomePage(pool, root, page, offset):
	ref = pool.request('GET', page)
	webpage = ref.data
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
				hall.days = parseHallPage(pool, root, hall.link, offset)
				dining.halls.append(hall)
	return dining
	
def parseHallPage(pool, root, page, offset):
	ref = pool.request('GET', page)
	webpage = ref.data
	soup = BeautifulSoup(webpage)
	frames = soup.find_all('frame')
	days = []
	for frame in frames:
		if frame['title'] == "left navigation menu":
			dayslink = root + frame['src']
			days = parseDaysPage(pool, root, dayslink, offset)
	return days

def parseDaysPage(pool, root, page, offset):
	ref = pool.request('GET', page)
	webpage = ref.data
	soup = BeautifulSoup(webpage)
	links = soup.find_all('a')
	days = []
	for link in links:
		print "opening page"
		if any(dayname in link.string for dayname in daynames):
			# Skip offset number of days
			if offset > 0:
				offset -= 1
				continue
			daylink = root + link['href']
			# Page is bad, contains space in url. urllib3 doesn't like it.
			daylink = daylink.replace(" ","")
			days.append(menuscraper.parseMenuPage(pool, root, daylink))
			days[len(days)-1].date = menuscraper.ascii(link.string)
			# If offset is at 0, then this is the day to return
			if offset == 0:
				days[0].ascii()
				print days[0].string()
				return days
	# DEBUG
	#print days[0].string()
	return days

def getData(offset = 0):
	root = "http://facilities.princeton.edu/dining/_Foodpro/"
	page = "http://facilities.princeton.edu/dining/_Foodpro/location.asp"
	# USE THIS POOL WHENEVER YOU MAKE A URL CALL! This saves the connections.
	pool = urllib3.PoolManager()
	data = parseHomePage(pool, root, page, offset)
	dininghalls = []
	for hall in data.halls:
		halldict = {}
		halldict['name'] = hall.name
		halldict['menus'] = []
		for menu in hall.days:
			menudict = {}
			menudict['date'] = menuscraper.ascii(menu.date)
			menudict['meals'] = []
			# Add the meals to the menu for the day
			menumeals = { 'breakfast': menu.breakfast, 'lunch': menu.lunch, 'dinner': menu.dinner }
			for (mealname, entreelist) in  menumeals.iteritems():
				mealdict = {}
				mealdict['type'] = mealname
				mealdict['entrees'] = []
				for entree in entreelist:
					mealdict['entrees'].append(entree.__dict__)
				menudict['meals'].append(mealdict)
			# Add the completed day's menu to the list of the hall's menus
			halldict['menus'].append(menudict)
		# Add the completed hall's week of menus to the list of halls
		dininghalls.append(halldict)
	return dininghalls

"""def pretty(d, indent=0):
	for key, value in d.iteritems():
	  print '\t' * indent + str(key)
	  if isinstance(value, dict):
		 pretty(value, indent+1)
	  else:
		 print '\t' * (indent+1) + str(value)
		 
data = getData(4)"""
