from datetime import datetime, date, time, timedelta

from google.appengine.ext import db
import tzsearch
import logging

# Identifiers for dining halls
halls = {
    'Butler & Wilson Colleges':'butlerwilson',
    'Forbes College':'forbes',
    'Rockefeller & Mathey Colleges':'rockymathey',
    'Whitman College':'whitman'
}

# Entree data type, keyed by name
class Entree(tzsearch.SearchableModel):
    date = db.DateProperty() # What day is this entree being served
    allergens = db.StringListProperty()
    ingredients = db.StringListProperty()
    name = db.StringProperty()
    protoname = db.StringProperty()
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
    
# Return all meals and entrees
def getMealsAndEntrees():
    meals = Meal.all().run()
    entrees = Entree.all().run()
    
    #db.delete(meals)
    #db.delete(entrees)
    return (meals, entrees)

# Return entrees that match a search query
def searchEntrees(q):
    d = date.today()
    dMin = d - timedelta(days=1)
    dMax = d + timedelta(days=5)
    query = Entree.all().search(q)
    query =  query.filter('date >=', dMin)
    query = query.filter('date <=', dMax)
    results = []
    for entree in query.run():
        if q.lower() in entree.name.lower():
            results.append(entree)
    return results

# Return all meals for a hall for a day
def getHallMeals(d, hall):
    meals = {}
    q = db.GqlQuery("SELECT * FROM Meal " +
                    "WHERE hall = :1 " +
                    "AND date = :2",
                    hall, d)
    for meal in q.run():
        if meal.type in meals:
            continue
        meals[meal.type] = Entree.get_by_id(meal.entreeIDs)
    return meals   

# Return menus for home page
def getMeals(d, type):
    menus = {}
    if type not in ['breakfast', 'lunch', 'dinner']:
        return []
    q = db.GqlQuery("SELECT * FROM Meal " + 
                    "WHERE type = :1 " + 
                    "AND date = :2 " +
                    "ORDER BY hall ASC",
                    type, d)
    for meal in q.run():
        if meal.hall in menus:
            continue
        menus[meal.hall] = Entree.get_by_id(meal.entreeIDs)
    return [menus['butlerwilson'], 
            menus['forbes'],
            menus['rockymathey'], 
            menus['whitman']]
