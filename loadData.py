import datetime
import logging
import pprint
from google.appengine.ext import db

import models
import menuparser
    
def load():
    # Fetch menu data
    data = menuparser.getData()
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
    db.put(entrees)
    
    return (meals, entrees)
    
def constructModels(hall, menu, meal):
    # Get entree models
    entrees = []
    entreeKeys = []
    for entree in meal['entrees']:
        key = entree['name']
        e = models.Entree(key_name=key)
        e.name = key
        e.allergens = entree['allergens']
        e.ingredients = entree['ingredients']
        entrees.append(e)
        entreeKeys.append(key)
    
    # Construct meals
    m = models.Meal()
    m.date = menu['date']
    m.hall = hall['name']
    m.type = meal['type']
    m.entreeKeys = entreeKeys

    return (m, entrees)
