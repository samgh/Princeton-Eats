from datetime import datetime, date, time
import logging
import pprint
import hashlib
from google.appengine.ext import db

import models
import menuparser
    
def load(offset=0):
    # Fetch menu data
    data = menuparser.getData(offset)
    meals = []
    entrees = []
    
    # Loop through dining halls
    for hall in data:
        # Loop through menus
        for menu in hall['menus']:
            # Loop through meals
            for meal in menu['meals']:
                (m, e) = constructModels(hall, menu, meal)
                # Put the meal just after deleting the old to reduce chance of inconsistent database
                db.delete(models.getMealsByDateHallType(m.date, m.hall, m.type))
                if m.entreeIDs != []:
                    db.put(m)
                meals.append(m)
                entrees = entrees + e
    
    # Put all meals and entrees in the database simultaneously for efficiency
    #db.put(meals)
    
    return (meals, entrees)
    
def constructModels(hall, menu, meal):
    # Get date
    dt = datetime.now()
    dateStr = menu['date'] + " %d" % dt.year
    dt = datetime.strptime(dateStr, "%A, %B %d %Y")
    d = dt.date()

    # Get entree models
    entrees = []
    entreeIDs = []
    hashes = []
    hallID = models.halls[hall['name']]
    for entree in meal['entrees']:
        key = entree['name']
        e = models.Entree()
        e.date = d
        e.name = entree['name']
        e.protoname = entree['name'] + "|" + hallID
        e.allergens = entree['allergens']
        e.ingredients = entree['ingredients']
        h = hashlib.md5()
        h.update(e.protoname)
        for s in e.ingredients:
            h.update(s)
        for s in e.allergens:
            h.update(s)
        e.hexhash = h.hexdigest()
        hashes.append(e.hexhash)
        entrees.append(e)

    # fetch entrees by hashes
    dbentrees = models.getEntreesByHashes(hashes)

    eKeys = []
    nentrees = []
    # remove duplicates and add to eKeys
    for entree in entrees:
        found = False
        for dbentree in dbentrees:
            if entree.hexhash == dbentree.hexhash:
                found = True
                eKeys.append(dbentree.key())
                break
        if not found:
            #print "Adding", entree.name
            eKeys.append(db.put(entree))

    entrees = nentrees
    # Add the entrees and get their IDs
    #eKeys = eKeys + db.put(entrees)
    for eKey in eKeys:
        entreeIDs.append(eKey.id())
    
    # Construct meals
    m = models.Meal()
    m.date = d
    m.hall = hallID
    m.type = meal['type']
    m.entreeIDs = entreeIDs

    return (m, entrees)