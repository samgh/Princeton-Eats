from datetime import datetime, date, time, timedelta
from google.appengine.api import memcache
from google.appengine.ext import db
import tzsearch
import logging
import re

# Identifiers for dining halls
halls = {
    'Butler & Wilson Colleges':'butlerwilson',
    'Forbes College':'forbes',
    'Rockefeller & Mathey Colleges':'rockymathey',
    'Whitman College':'whitman'
}

# Ratings for a given protoname.
class Rating(db.Model):
    upvotes = db.IntegerProperty()
    upvoters = db.ListProperty(str)
    downvotes = db.IntegerProperty()
    downvoters = db.ListProperty(str)

# Entree data type, keyed by name
class Entree(tzsearch.SearchableModel):
    date = db.DateProperty() # What day is this entree being served
    allergens = db.StringListProperty()
    ingredients = db.StringListProperty()
    name = db.StringProperty()
    protoname = db.StringProperty()
    hexhash = db.StringProperty()
    hall = db.StringProperty() # Dining hall
    type = db.StringProperty() # breakfast, lunch or dinner

    def getDownvotes(self):
        r = memcache.get(self.protoname)
        if r == None:
            r = Rating.get_or_insert(self.protoname)
            memcache.set(self.protoname, r)
        if r.downvotes == None:
            return 0
        return r.downvotes

    def getUpvotes(self):
        r = memcache.get(self.protoname)
        if r == None:
            r = Rating.get_or_insert(self.protoname)
            memcache.set(self.protoname, r)
        if r.upvotes == None:
            return 0
        return r.upvotes

    def checkUserVote(self, ip):
        r = memcache.get(self.protoname)
        if r == None:
            r = Rating.get_or_insert(self.protoname)
            memcache.set(self.protoname, r)
        self.vote = 0
        if ip in r.upvoters:
            self.vote = 1
        elif ip in r.downvoters:
            self.vote = -1

    def formatted_date(self):
        return self.date.strftime('%A, %B %d')
    def formatted_url_date(self):
        return self.date.strftime('%-m/%d/%Y')
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s</b></p>' % self.name
        html = html + '<p>%s</p>' % self.allergens
        html = html + '<p>%s</p>' % self.ingredients
        html = html + '</div>'
        return html

# Meal data type
class Meal(db.Model):
    date = db.DateProperty()   # What day is this meal associated with
    entreeIDs = db.ListProperty(int)
    hall = db.StringProperty() # Dining hall
    type = db.StringProperty() # breakfast, lunch or dinner
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s, %s, %s</b></p>' % (self.hall, self.type, self.date)
        html = html + '<p>%s</p>' % self.entreeIDs
        html = html + '</div>'
        return html
    
# Return entree by id
def getEntreeById(id, ip):
    entree = Entree.get_by_id(id)
    entree.checkUserVote(ip)
    return entree

# Vote on entree by id
def addEntreeVote(id, ip, vote):
    # Get entree
    entree = getEntreeById(id, ip)
    r = memcache.get(entree.protoname)
    if r == None:
        r = Rating.get_or_insert(self.protoname)
    
    # Remove old votes
    if ip in r.upvoters:
        r.upvoters.remove(ip)
    if ip in r.downvoters:
        r.downvoters.remove(ip)

    # Apply new vote
    if vote == 1:
        r.upvoters.append(ip)
    elif vote == -1:
        r.downvoters.append(ip)

    # Update
    #del r.vote
    r.upvoters.sort()
    r.downvoters.sort()
    r.upvotes = len(r.upvoters)
    r.downvotes = len(r.downvoters)
    r.put()
    # This overwrites the old version, so the new votes are in the cache.
    memcache.set(entree.protoname, r)

# Return all meals and entrees
def getMealsAndEntrees():
    meals = Meal.all().run()
    entrees = Entree.all().run()
    
    #db.delete(meals)
    #db.delete(entrees)
    return (meals, entrees)

def getEntreesByHashes(hashes):
    q = db.GqlQuery("SELECT * FROM Entree " +
                    "WHERE hexhash IN :1 ",
                    hashes)
    entrees = []
    for entree in q.run():
        entrees.append(entree)
    return entrees

def getMealByDateHallType(date, hall, mtype):
    q = db.GqlQuery("SELECT * FROM Meal " +
        "WHERE hall = :1 " +
        "AND date = :2 " +
        "AND type = :3 ",
        hall, date, mtype)
    return q.get()

def delOutdatedEntries():
    d = date.today()
    dMin = d- timedelta(days=1) #days=1
    query = Entree.all()
    query = query.filter('date <', dMin)
    db.delete(query.run())
    query = Meal.all()
    query.filter('date <', dMin)
    db.delete(query.run())
    memcache.flush_all()

# Return entrees that match a search query
def searchEntrees(q, ip):
    # Sanitize input
    # Do nothing for null string
    if not q or re.search('\w', q) is None:
        return []
    dhalls = ['butlerwilson', 'forbes', 'rockymathey', 'whitman']
    mtypes = ["breakfast", "lunch", "dinner"]
    q = re.sub("[^\w']", ' ', q)

    sKey = "search_query" + q
    results = memcache.get(sKey)
    if results == None:
        d = date.today()
        dMin = d - timedelta(days=1)
        dMax = d + timedelta(days=5)
        query = Entree.all().search(q)
        query =  query.filter('date >=', dMin)
        query = query.filter('date <=', dMax)
        results = []
        for mtype in mtypes:
            for dhall in dhalls:
                for entree in query.run():
                    if entree.type == mtype and entree.hall == dhall\
                    and q.lower() in entree.name.lower():
                        if entree not in results:
                            results.append(entree)
        memcache.set(sKey, results)

    for entree in results:
        entree.checkUserVote(ip)
    # Sort by date
    results.sort(key=lambda r: r.date)
    return results

# Return all meals for a hall for a day
def getHallMeals(d, hall):
    meals = {}
    q = db.GqlQuery("SELECT * FROM Meal " +
                    "WHERE hall = :1 " +
                    "AND date = :2",
                    hall, d)
    
    # Set meal dictionaries
    for meal in q.run():
        if meal.type in meals:
            continue
        meals[meal.type] = Entree.get_by_id(meal.entreeIDs)

    # Set hall meal array
    hallMeals = []
    if 'breakfast' in meals:
        hallMeals.append({ 
            'type':'breakfast', 
            'entrees':meals['breakfast']
        })
    if 'lunch' in meals:
        hallMeals.append({ 
            'type':'lunch', 
            'entrees':meals['lunch']
        })
    if 'dinner' in meals:
        hallMeals.append({ 
            'type':'dinner',
            'entrees':meals['dinner']
        })

    return hallMeals

# Return menus for home page
def getMeals(d, type):
    if type not in ['breakfast', 'lunch', 'dinner']:
        return []
    cKey = str(d)+str(type)
    menuArray = memcache.get(cKey)
    if menuArray != None:
        return menuArray

    menus = {}
    menulist = []
    q = db.GqlQuery("SELECT * FROM Meal " + 
                    "WHERE type = :1 " + 
                    "AND date = :2 " +
                    "ORDER BY hall ASC",
                    type, d)
    for meal in q.run():
        menulist.append(meal)

    for meal in menulist:
        if meal.hall in menus:
            continue
        menus[meal.hall] = Entree.get_by_id(meal.entreeIDs)


    # Attempt to add data to an array of menus
    menuArray = []
    try:
        menuArray = [
            menus['butlerwilson'], 
            menus['forbes'],
            menus['rockymathey'], 
            menus['whitman']
        ]
    except Exception, e:
        menuArray = [
            [], [], [], []
        ]
    # This cache entry is valid for 3 hours.
    memcache.set(cKey, menuArray)  
    return menuArray
