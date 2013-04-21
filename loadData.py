from datetime import datetime, date, time
import logging
import pprint
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
                meals.append(m)
                entrees = entrees + e
    
    # Put all meals and entrees in the database simultaneously for efficiency
    db.put(meals)
    
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
    hallID = models.halls[hall['name']]
    for entree in meal['entrees']:
        key = entree['name']
        e = models.Entree()
        e.date = d
        e.name = entree['name']
        e.protoname = entree['name'] + "|" + hallID
        e.allergens = entree['allergens']
        e.ingredients = entree['ingredients']
        entrees.append(e)

    # Add the entrees and get their IDs
    eKeys = db.put(entrees)
    for eKey in eKeys:
        entreeIDs.append(eKey.id())
    
    # Construct meals
    m = models.Meal()
    m.date = d
    m.hall = hallID
    m.type = meal['type']
    m.entreeIDs = entreeIDs

    return (m, entrees)